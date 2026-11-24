[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$AppDir,
    [Parameter(Mandatory)][string]$SdkBin,
    [Parameter(Mandatory)][string]$OutputDir,
    [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9.-]{3,50}$')][string]$IdentityName,
    [Parameter(Mandatory)][string]$Publisher,
    [string]$PublisherDisplayName,
    [Parameter(Mandatory)][ValidatePattern('^[1-9]?\d{1,4}\.\d{1,5}\.\d{1,5}\.0$')][string[]]$Version,
    [switch]$SignForTest
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($PublisherDisplayName)) {
    if (-not $SignForTest) {
        throw 'Pass -PublisherDisplayName from the app Product identity page in Partner Center.'
    }
    $PublisherDisplayName = 'PDF Designer'
}
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$source = git -C $repo rev-parse HEAD
if ($LASTEXITCODE -or (git -C $repo status --porcelain)) {
    throw 'Package from a clean source checkout.'
}
$app = (Resolve-Path -LiteralPath $AppDir).Path
$sdk = (Resolve-Path -LiteralPath $SdkBin).Path
$makeappx = Join-Path $sdk 'makeappx.exe'
$signtool = Join-Path $sdk 'signtool.exe'
$output = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDir)
if (Test-Path -LiteralPath $output) { throw 'Choose a new output directory for each packaging run.' }
if ($output.StartsWith($app.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The package output cannot be inside the input app.'
}
if ($SignForTest -and $Publisher -cne 'CN=PDF Designer Release QA') {
    throw 'The local signing switch is reserved for the provisional QA publisher.'
}
$required = @(
    'PDF Designer.exe', 'resources/app.asar', 'LICENSE.electron.txt', 'LICENSES.chromium.html',
    'resources/runtime/pdf-designer-runtime/pdf-designer-runtime.exe',
    'resources/runtime/pdf-designer-runtime/_internal/pdf_tool/share/profiles/you-resume.example.json',
    'resources/runtime/pdf-designer-runtime/notices/Python-LICENSE.txt',
    'resources/workspace-seed/users/examples.json'
)
foreach ($file in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $app $file) -PathType Leaf)) {
        throw "The unpacked Electron runtime is missing $file."
    }
}
$files = @(Get-ChildItem -LiteralPath $app -Recurse -File -Force)
if (-not ($files | Where-Object FullName -Match '[\\/]chrome-win[^\\/]*[\\/]chrome\.exe$')) {
    throw 'The unpacked runtime is missing its bundled Chromium.'
}
if ($files | Where-Object FullName -Match '[\\/]browsers[\\/].*[\\/]setup\.exe$') {
    throw 'Build the release runtime again. The Chromium setup executable is unnecessary in the MSIX payload.'
}
if ($files | Where-Object { $_.Name -match '(^\.env($|\.)|\.(pfx|p12|pem|key)$|^runtime-ready\.txt$)' }) {
    throw 'The unpacked app contains unexpected private material.'
}
New-Item -ItemType Directory -Path $output | Out-Null

Add-Type -AssemblyName System.Drawing
$image = [Drawing.Image]::FromFile((Join-Path $repo 'src/pdf_tool/static/hub-app-icon.png'))
try {
    foreach ($size in 44, 50, 150) {
        $bitmap = [Drawing.Bitmap]::new($size, $size)
        $graphics = [Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.DrawImage($image, 0, 0, $size, $size)
            $bitmap.Save((Join-Path $output "Logo$size.png"), [Drawing.Imaging.ImageFormat]::Png)
        } finally {
            $graphics.Dispose()
            $bitmap.Dispose()
        }
    }
} finally {
    $image.Dispose()
}

$certificate = $null
if ($SignForTest) {
    $key = [Security.Cryptography.RSA]::Create(3072)
    $certRequest = [Security.Cryptography.X509Certificates.CertificateRequest]::new(
        $Publisher, $key, [Security.Cryptography.HashAlgorithmName]::SHA256,
        [Security.Cryptography.RSASignaturePadding]::Pkcs1
    )
    $usage = [Security.Cryptography.OidCollection]::new()
    [void]$usage.Add([Security.Cryptography.Oid]::new('1.3.6.1.5.5.7.3.3'))
    $certRequest.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509EnhancedKeyUsageExtension]::new($usage, $true)
    )
    $certRequest.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509KeyUsageExtension]::new(
            [Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature, $true
        )
    )
    $certRequest.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509BasicConstraintsExtension]::new($false, $false, 0, $true)
    )
    $certificate = $certRequest.CreateSelfSigned([DateTimeOffset]::UtcNow.AddMinutes(-5), [DateTimeOffset]::UtcNow.AddDays(30))
    $password = [Guid]::NewGuid().ToString('N')
    $privateCert = Join-Path ([IO.Path]::GetTempPath()) ("pdf-designer-" + [Guid]::NewGuid().ToString('N') + '.pfx')
}

try {
    if ($certificate) {
        [IO.File]::WriteAllBytes($privateCert, $certificate.Export('Pfx', $password))
        [IO.File]::WriteAllBytes((Join-Path $output 'PDF-Designer-QA.cer'), $certificate.Export('Cert'))
    }
    $payload = foreach ($file in $files) {
        $relative = [IO.Path]::GetRelativePath($app, $file.FullName)
        '"' + $file.FullName + '" "' + $relative + '"'
    }
    $escapedPublisher = [Security.SecurityElement]::Escape($Publisher)
    $escapedPublisherDisplayName = [Security.SecurityElement]::Escape($PublisherDisplayName)
    foreach ($number in $Version) {
        if ([version]$number -lt [version]'0.1.0.0' -or ($number.Split('.') | Where-Object { [int]$_ -gt 65535 })) {
            throw "Invalid Store package version: $number"
        }
        $manifest = Join-Path $output "AppxManifest-$number.xml"
        @"
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">
  <Identity Name="$IdentityName" Publisher="$escapedPublisher" Version="$number" ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>PDF Designer</DisplayName>
    <PublisherDisplayName>$escapedPublisherDisplayName</PublisherDisplayName>
    <Description>Local document designer and PDF exporter.</Description>
    <Logo>Assets\Logo50.png</Logo>
  </Properties>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.19041.0" MaxVersionTested="10.0.26100.0" />
  </Dependencies>
  <Resources><Resource Language="en-us" /></Resources>
  <Applications>
    <Application Id="PDFDesigner" Executable="PDF Designer.exe" EntryPoint="windows.fullTrustApplication">
      <uap:VisualElements DisplayName="PDF Designer" Description="Local document designer and PDF exporter."
        Square150x150Logo="Assets\Logo150.png" Square44x44Logo="Assets\Logo44.png" BackgroundColor="transparent" />
    </Application>
  </Applications>
  <Capabilities><rescap:Capability Name="runFullTrust" /></Capabilities>
</Package>
"@ | Set-Content -LiteralPath $manifest -Encoding utf8
        $provenance = Join-Path $output "release-source-$number.json"
        [ordered]@{
            source = $source
            version = $number
            sdk = (Get-Item -LiteralPath $makeappx).VersionInfo.FileVersion
            runtime = Get-Content -LiteralPath (Join-Path $app 'resources/runtime/pdf-designer-runtime/notices/runtime-versions.txt')
        } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $provenance -Encoding utf8
        $mapping = Join-Path $output "mapping-$number.txt"
        @(
            '[Files]'
            $payload
            '"' + $manifest + '" "AppxManifest.xml"'
            '"' + $provenance + '" "resources\release-source.json"'
            foreach ($size in 44, 50, 150) { '"' + (Join-Path $output "Logo$size.png") + '" "Assets\Logo' + $size + '.png"' }
        ) | Set-Content -LiteralPath $mapping -Encoding utf8BOM
        $package = Join-Path $output "PDF-Designer-$number-x64.msix"
        & $makeappx pack /f $mapping /p $package /h SHA256
        if ($LASTEXITCODE) { throw "MakeAppx failed for $number with code $LASTEXITCODE." }
        if ($certificate) {
            & $signtool sign /fd SHA256 /f $privateCert /p $password $package
            if ($LASTEXITCODE) { throw "SignTool failed for $number with code $LASTEXITCODE." }
        }
        Get-FileHash -LiteralPath $package -Algorithm SHA256
    }
} finally {
    if ($certificate) {
        if (Test-Path -LiteralPath $privateCert) { Remove-Item -LiteralPath $privateCert }
        $certificate.Dispose()
        $key.Dispose()
    }
}
