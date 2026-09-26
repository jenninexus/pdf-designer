# Private collage source assets must stay with their source HTML

## Hook

The Hub discovers a private collage page, but its image cells show filenames or broken-image icons while
an exported copy of the same images still exists.

## Root cause

`_exports/` is a deliverable boundary, not a source-media store. Relative URLs in
`collages/<project>/.../*.html` resolve from the source page, so preserving the only PNG copy under
`_exports/<profile>/collages/<project>/` leaves the page discoverable but visually broken. A related trap
is generating a favorite page one level away from `images/` while retaining a candidate page's deeper
`../../` references.

## Guard

1. Keep private source media under `collages/<project>/` or `collages/<project>/images/`; the entire tree
   is already gitignored and is still served by the local Hub.
2. Copy outputs into `_exports/`; do not move away the source page's only media copy.
3. Resolve image paths from the HTML file's actual directory, not from the project root.
4. Before closeout, load the page through `127.0.0.1:8787` and require every local image to have a
   successful HTTP response and `naturalWidth > 0`.

## Why this is safe

Git privacy and local visibility are independent: ignored content remains readable by the local Hub but
cannot enter a normal commit. Do not repair a private preview by moving real media into tracked examples.
