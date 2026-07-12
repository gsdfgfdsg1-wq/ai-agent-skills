# Usage Examples

## 1. Single IP lookup

```bash
python skills/ip-geo-lookup/scripts/ip_geo.py 8.8.8.8
```

Output:

```text
  8.8.8.8:
    country: United States
    regionName: Virginia
    city: Ashburn
    lat: 39.03
    lon: -77.5
    isp: Google LLC
    org: Google Public DNS
    as: AS15169 Google LLC
```

## 2. Batch from file

```bash
python skills/ip-geo-lookup/scripts/ip_geo.py --file suspicious_ips.txt
```

## 3. JSON output

```bash
python skills/ip-geo-lookup/scripts/ip_geo.py 8.8.8.8 --json
```

## 4. Custom fields

```bash
python skills/ip-geo-lookup/scripts/ip_geo.py 8.8.8.8 --fields country,city,isp
```

## 5. Verify your own public IP

```bash
python skills/ip-geo-lookup/scripts/ip_geo.py $(curl -s ifconfig.me)
```
