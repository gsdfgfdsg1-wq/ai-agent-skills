# Usage Examples

## 1. Single image metadata

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py photo.jpg
```

Output:

```text
photo.jpg: JPEG 4000x3000 3.2 MB
  Make: Canon
  Model: EOS R5
  DateTime: 2025:06:15 14:30:00
  Orientation: 1
```

## 2. Scan a directory

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py assets/
```

Recursively scans all supported image files and reports metadata.

## 3. JSON output

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py assets/ --json
```

Returns JSON array with file, format, width, height, bit_depth, file_size, file_size_human, and optionally exif.

## 4. Top N largest images

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py . --top 10
```

Shows only the 10 largest images, sorted by file size.

## 5. Skip EXIF for speed

```bash
python skills/image-meta-scraper/scripts/image_meta_scraper.py large_dataset/ --no-exif
```

Skips EXIF parsing for faster scanning of large image collections.
