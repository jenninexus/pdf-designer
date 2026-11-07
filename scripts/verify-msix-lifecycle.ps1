# Run in an offline, disposable Windows 10/11 x64 guest with a signed-in desktop.
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Baseline,
    [Parameter(Mandatory)][string]$Update,
    [Parameter(Mandatory)][string]$Certificate,
    [Parameter(Mandatory)][string]$EvidenceDir,
    [ValidateRange(30, 600)][int]$TimeoutSeconds = 180
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$identity = 'JenniNexus.PDFDesigner.QA'
$workspace = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'PDF Designer'
$exports = Join-Path $workspace 'release-test-exports'
$doc = 'examples/profiles/default-resume/default-resume.html'
$receipt = [ordered]@{ started = [DateTime]::UtcNow.ToString('o'); checks = [ordered]@{} }
$certificatePath = $null
$current = $null
$socket = $null

function Require([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Wait-For([scriptblock]$Probe, [string]$Message) {
    $clock = [Diagnostics.Stopwatch]::StartNew()
    while ($clock.Elapsed.TotalSeconds -lt $TimeoutSeconds) {
        $value = & $Probe
        if ($value) { return $value }
        Start-Sleep -Milliseconds 250
    }
    throw $Message
}

function Invoke-Browser([string]$Expression) {
    $payload = @{
        id = 1; method = 'Runtime.evaluate'
        params = @{ expression = $Expression; awaitPromise = $true; returnByValue = $true }
    } | ConvertTo-Json -Depth 5 -Compress
    $cancel = [Threading.CancellationTokenSource]::new([TimeSpan]::FromSeconds($TimeoutSeconds))
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
        [void]$socket.SendAsync([ArraySegment[byte]]::new($bytes), 'Text', $true, $cancel.Token).GetAwaiter().GetResult()
        $buffer = New-Object byte[] 8192
        do {
            $stream = [IO.MemoryStream]::new()
            try {
                do {
                    $part = $socket.ReceiveAsync([ArraySegment[byte]]::new($buffer), $cancel.Token).GetAwaiter().GetResult()
                    if ($part.MessageType -eq 'Close') { throw 'Electron closed the QA browser connection.' }
                    $stream.Write($buffer, 0, $part.Count)
                } until ($part.EndOfMessage)
                $response = [Text.Encoding]::UTF8.GetString($stream.ToArray()) | ConvertFrom-Json
            } finally {
                $stream.Dispose()
            }
        } until ($response.PSObject.Properties['id'])
        if ($response.PSObject.Properties['error']) { throw ($response.error | ConvertTo-Json -Compress) }
        if ($response.result.PSObject.Properties['exceptionDetails']) {
            throw ($response.result.exceptionDetails | ConvertTo-Json -Depth 5 -Compress)
        }
        if ($response.result.result.PSObject.Properties['value']) { return $response.result.result.value }
    } finally {
        $cancel.Dispose()
    }
}

function Start-InstalledApp($Package) {
    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $debugPort = $listener.LocalEndpoint.Port
    $listener.Stop()
    $appId = $Package.PackageFamilyName + '!PDFDesigner'
    $appPid = [MsixQa.Activation]::Launch($appId, "--remote-debugging-port=$debugPort --remote-debugging-address=127.0.0.1")
    $appExe = Join-Path $Package.InstallLocation 'PDF Designer.exe'
    $runtimeExe = Join-Path $Package.InstallLocation 'resources\runtime\pdf-designer-runtime\pdf-designer-runtime.exe'
    $runtime = Wait-For {
        Get-CimInstance Win32_Process -Filter "Name='pdf-designer-runtime.exe'" |
            Where-Object { $_.ParentProcessId -eq $appPid -and $_.ExecutablePath -eq $runtimeExe }
    } 'Installed app did not start its bundled runtime.'
    Require ((Get-Process -Id $appPid).Path -eq $appExe) 'Activation did not start the installed Electron executable.'
    $target = Wait-For {
        try {
            Invoke-RestMethod "http://127.0.0.1:$debugPort/json/list" -TimeoutSec 2 |
                ForEach-Object { $_ } | Where-Object { $_.type -eq 'page' -and $_.url -match '^http://127\.0\.0\.1:\d+/' } |
                Select-Object -First 1
        } catch { }
    } 'Electron did not open the installed Hub.'
    $script:socket = [Net.WebSockets.ClientWebSocket]::new()
    $connect = [Threading.CancellationTokenSource]::new([TimeSpan]::FromSeconds($TimeoutSeconds))
    try { [void]$socket.ConnectAsync([uri]$target.webSocketDebuggerUrl, $connect.Token).GetAwaiter().GetResult() }
    finally { $connect.Dispose() }
    $origin = ([uri]$target.url).GetLeftPart('Authority')
    Wait-For { Invoke-Browser "document.readyState === 'complete' && !!document.querySelector('#main')" } 'Hub failed to load.' | Out-Null
    [pscustomobject]@{ appPid = $appPid; runtimePid = $runtime.ProcessId; origin = $origin; runtime = $runtimeExe }
}

function Close-InstalledApp($App) {
    if ($script:socket) {
        $script:socket.Dispose()
        $script:socket = $null
    }
    $process = Get-Process -Id $App.appPid -ErrorAction SilentlyContinue
    if ($process) {
        Require ($process.CloseMainWindow()) 'Could not close the installed Electron window normally.'
        Require ($process.WaitForExit($TimeoutSeconds * 1000)) 'Electron did not exit after closing its window.'
    }
    Wait-For { -not (Get-Process -Id $App.runtimePid -ErrorAction SilentlyContinue) } 'The bundled runtime survived Electron exit.' | Out-Null
}

function Assert-Blocked([string]$Url, [hashtable]$Headers, [string]$Method = 'GET') {
    $request = [Net.HttpWebRequest][Net.WebRequest]::Create($Url)
    $request.Method = $Method
    $request.Timeout = 10000
    if ($Headers.ContainsKey('Host')) { $request.Host = $Headers.Host }
    if ($Headers.ContainsKey('Origin')) { $request.Headers['Origin'] = $Headers.Origin }
    if ($Method -eq 'POST') {
        $request.ContentType = 'application/json'
        $request.ContentLength = 0
    }
    try {
        $request.GetResponse().Dispose()
        throw 'A foreign request reached the Hub.'
    } catch [Net.WebException] {
        $response = $_.Exception.Response
        Require ($response -and [int]$response.StatusCode -eq 403) 'Foreign request did not receive 403.'
        $response.Dispose()
    }
}

$evidence = New-Item -ItemType Directory -Path $EvidenceDir -Force
$receiptFile = Join-Path $evidence.FullName 'lifecycle.json'
Require (-not (Test-Path -LiteralPath $receiptFile)) 'Choose a fresh evidence directory.'
try {
    $os = Get-CimInstance Win32_OperatingSystem
    Require ($os.OSArchitecture -match '64' -and [int]$os.BuildNumber -ge 19041) 'A supported Windows x64 guest is required.'
    $receipt.os = [ordered]@{ caption = $os.Caption; build = $os.BuildNumber; architecture = $os.OSArchitecture }
    $receipt.workspace = $workspace
    foreach ($tool in 'python','py','node','npm','git') {
        $command = Get-Command $tool -ErrorAction SilentlyContinue
        Require (-not $command) "Clean guest has $tool on PATH."
    }
    Require (-not (Get-NetRoute -ErrorAction SilentlyContinue | Where-Object DestinationPrefix -In '0.0.0.0/0','::/0')) 'Disconnect guest networking before the run.'
    Require (-not (Get-AppxPackage -Name $identity)) 'The provisional package is already installed.'
    Require (-not (Test-Path -LiteralPath $workspace)) 'The workspace already exists.'
    $receipt.checks.preflight = 'offline, no toolchain, no prior package or workspace'

    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
namespace MsixQa {
    [ComImport, Guid("2e941141-7f97-4756-ba1d-9decde894a3d"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IActivationManager {
        void ActivateApplication([MarshalAs(UnmanagedType.LPWStr)] string appId,
            [MarshalAs(UnmanagedType.LPWStr)] string args, uint options, out uint pid);
    }
    [ComImport, Guid("45ba127d-10a8-46ea-8ab7-56ea9078943c")]
    class ActivationManager { }
    public static class Activation {
        public static uint Launch(string appId, string args) {
            uint pid;
            ((IActivationManager)new ActivationManager()).ActivateApplication(appId, args, 0, out pid);
            return pid;
        }
    }
}
'@
    $cert = [Security.Cryptography.X509Certificates.X509Certificate2]::new((Resolve-Path -LiteralPath $Certificate).Path)
    Require ($cert.Subject -eq 'CN=PDF Designer Release QA') 'The certificate must be the provisional QA publisher.'
    $certificatePath = "Cert:\LocalMachine\TrustedPeople\$($cert.Thumbprint)"
    Require (-not (Test-Path -LiteralPath $certificatePath)) 'The QA certificate is already trusted.'
    Import-Certificate -FilePath $Certificate -CertStoreLocation Cert:\LocalMachine\TrustedPeople | Out-Null

    $receipt.baselineSha256 = (Get-FileHash -LiteralPath $Baseline).Hash
    $receipt.updateSha256 = (Get-FileHash -LiteralPath $Update).Hash
    Add-AppxPackage -Path (Resolve-Path -LiteralPath $Baseline).Path
    $first = Get-AppxPackage -Name $identity
    Require ([bool]$first) 'The baseline package was not registered.'
    $receipt.checks.install = $first.PackageFullName
    $current = Start-InstalledApp $first
    $receipt.runtime = $current.runtime
    Require (Test-Path -LiteralPath (Join-Path $workspace $doc)) 'First launch did not seed Jane Example.'
    $sample = Invoke-Browser @'
(async () => {
  const documentPath = 'examples/profiles/default-resume/default-resume.html';
  const entry = DOCS.find(item => item.path === documentPath);
  if (!entry) return false;
  const frame = document.querySelector('#main');
  await new Promise(resolve => {
    frame.addEventListener('load', resolve, { once: true });
    select(entry, null);
  });
  return frame.contentDocument.body.innerText.includes('Jane Example');
})()
'@
    Require ($sample -eq $true) 'The installed Hub did not preview Jane Example.'
    $receipt.checks.firstRun = 'fictional Jane Example opened in the packaged Hub'

    Assert-Blocked "$($current.origin)/api/vault-overview" @{ Host = 'fictional.invalid' }
    Assert-Blocked "$($current.origin)/api/save-starter" @{ Origin = 'https://fictional.invalid' } 'POST'
    $attack = Join-Path $workspace 'release-fixture.html'
    '<div id="fixture">Fictional</div><script>document.body.dataset.executed="true";fetch("/api/vault-overview")</script>' |
        Set-Content -LiteralPath $attack -Encoding UTF8
    $blocked = Invoke-Browser @'
(async () => {
  const frame = document.createElement('iframe');
  document.body.append(frame);
  await new Promise(resolve => { frame.onload = resolve; frame.src = '/release-fixture.html'; });
  return frame.contentDocument.querySelector('#fixture').textContent === 'Fictional' &&
    frame.contentDocument.body.dataset.executed === undefined;
})()
'@
    Require ($blocked -eq $true) 'The packaged preview executed document JavaScript.'
    $receipt.checks.packagedPrivacy = 'foreign Host and Origin refused, document script blocked in Electron'

    $inputHtml = '<h1>Fictional Release Tester</h1><h2>Job Title</h2><p>Designer</p><h2>Work Experience</h2><p>Example Studio</p><h2>Education</h2><p>Example School</p>'
    $upload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($inputHtml))
    $draft = Invoke-RestMethod "$($current.origin)/api/import-resume" -Method Post -ContentType 'application/json' -Body (
        @{ files = @(@{ name = 'fictional.html'; contentBase64 = $upload }); slug = 'fictional-release' } | ConvertTo-Json -Depth 5
    )
    Require ($draft.ok -eq $true) "Fictional resume import failed: $($draft | ConvertTo-Json -Depth 5 -Compress)"
    $save = Invoke-RestMethod "$($current.origin)/api/save-starter" -Method Post -ContentType 'application/json' -Body (
        @{ draft = $draft.draft; slug = 'fictional-release' } | ConvertTo-Json -Depth 20
    )
    Require ($save.ok -eq $true) "Fictional starter creation failed: $($save | ConvertTo-Json -Depth 5 -Compress)"
    $receipt.checks.importAndSave = 'fictional-release'

    $artifactHashes = [ordered]@{}
    foreach ($theme in 'light','dark') {
        $body = @{ doc = $doc; format = "pdf-$theme"; outDir = $exports } | ConvertTo-Json -Compress
        $result = Invoke-RestMethod "$($current.origin)/api/export" -Method Post -ContentType 'application/json' -Body $body -TimeoutSec $TimeoutSeconds
        Require ($result.ok -eq $true) "Packaged $theme export failed: $($result | ConvertTo-Json -Compress)"
        $file = $result.outputs[0]
        Require ((Get-Item -LiteralPath $file).Length -gt 1000) "Missing $theme PDF."
        $artifactHashes[$theme] = (Get-FileHash -LiteralPath $file).Hash
        Copy-Item -LiteralPath $file -Destination $evidence.FullName
    }
    Require ($artifactHashes.light -ne $artifactHashes.dark) 'Light and dark output bytes match.'
    $receipt.checks.exports = $artifactHashes
    $prefKey = 'pdf-designer.hub.profileFilter'
    $null = Invoke-Browser "localStorage.setItem('$prefKey','fictional-release')"
    $workspaceHashes = @(Get-ChildItem -LiteralPath $workspace -Recurse -File | Get-FileHash)
    $initialOrigin = $current.origin
    Close-InstalledApp $current
    $current = $null
    $receipt.checks.baselineShutdown = 'bundled runtime stopped on window close'

    Add-AppxPackage -Path (Resolve-Path -LiteralPath $Update).Path
    $second = Get-AppxPackage -Name $identity
    Require ($second.PackageFamilyName -eq $first.PackageFamilyName -and $second.Version -gt $first.Version) 'The second package did not upgrade the first.'
    $current = Start-InstalledApp $second
    Require ($current.origin -eq $initialOrigin) 'The updated app did not reopen the saved Hub origin.'
    Require ((Invoke-Browser "localStorage.getItem('$prefKey')") -eq 'fictional-release') 'A Hub preference was lost during update.'
    $receipt.checks.update = $second.PackageFullName
    Close-InstalledApp $current
    $current = $null
    $receipt.checks.updateShutdown = 'updated bundled runtime stopped on window close'

    Remove-AppxPackage -Package $second.PackageFullName
    Require (-not (Get-AppxPackage -Name $identity)) 'The application registration remains after uninstall.'
    foreach ($item in $workspaceHashes) {
        Require ((Get-FileHash -LiteralPath $item.Path).Hash -eq $item.Hash) 'A workspace file changed or disappeared.'
    }
    $receipt.checks.uninstall = "$($workspaceHashes.Count) workspace files retained byte-for-byte"
    $receipt.status = 'passed'
} catch {
    $receipt.status = 'failed'
    $receipt.error = $_.ToString()
    $receipt.stack = $_.ScriptStackTrace
    throw
} finally {
    try {
        if ($current) { Close-InstalledApp $current }
        if ($certificatePath -and (Test-Path -LiteralPath $certificatePath)) {
            Remove-Item -LiteralPath $certificatePath
        }
    } finally {
        $receipt.finished = [DateTime]::UtcNow.ToString('o')
        $receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $receiptFile -Encoding UTF8
    }
}
