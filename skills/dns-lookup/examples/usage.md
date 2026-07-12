# Usage Examples

## 1. Basic lookup (A, AAAA, MX, NS, TXT)

```bash
python skills/dns-lookup/scripts/dns_lookup.py example.com
```

Output:

```text
DNS Lookup for example.com

  A:
    93.184.216.34
  AAAA:
    2606:2800:220:1:248:1893:25c8:1946
  MX:
    {'priority': 0, 'host': 'mail.example.com'}
  NS:
    ns1.example.com
  TXT:
    v=spf1 -all
```

## 2. Specific record type

```bash
python skills/dns-lookup/scripts/dns_lookup.py example.com --type MX
```

## 3. All record types

```bash
python skills/dns-lookup/scripts/dns_lookup.py example.com --all
```

## 4. JSON output

```bash
python skills/dns-lookup/scripts/dns_lookup.py example.com --json
```

## 5. Check SPF/DKIM/DMARC

```bash
python skills/dns-lookup/scripts/dns_lookup.py example.com --type TXT
```

Look for `v=spf1`, `v=DKIM1`, and `v=DMARC1` in TXT records.
