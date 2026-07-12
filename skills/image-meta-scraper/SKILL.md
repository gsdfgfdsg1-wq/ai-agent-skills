---
name: image-meta-scraper
description: Extract image metadata including dimensions, format, file size, and basic EXIF data from JPEG/PNG/GIF/BMP/WebP files without external dependencies.
license: MIT
---

# Image Meta Scraper

> Pull metadata from images — dimensions, format, EXIF — no PIL or ImageMagick required.

## When to Use / Triggers

- Audit image assets for dimensions and file sizes.
- Extract EXIF data from photos for privacy review.
- Batch-report image metadata for content management.
- CI: validate image dimensions and sizes before deployment.

## Capabilities

- Reads JPEG, PNG, GIF, BMP, and WebP file headers natively (no PIL).
- Extracts: image dimensions (width x height), format, bit depth, file size.
- Parses JPEG EXIF data (camera make/model, date, GPS coordinates, orientation).
- `--json` for machine-readable output.
- Recursively scans directories.
- `--top N` to limit results.

## Usage

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py photo.jpg
python skills/image-meta-scraper/scripts/image_meta_scraper.py assets/ --json
python skills/image-meta-scraper/scripts/image_meta_scraper.py . --top 20
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/image_meta_scraper.py --help` for all options.
