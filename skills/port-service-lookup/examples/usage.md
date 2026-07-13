# Port Service Lookup Examples

Look up the standard HTTPS mapping:

```bash
python skills/port-service-lookup/scripts/port_service_lookup.py 443
```

Look up DNS and keep only its UDP mapping:

```bash
python skills/port-service-lookup/scripts/port_service_lookup.py dns --protocol udp
```

Use JSON output in an automation workflow:

```bash
python skills/port-service-lookup/scripts/port_service_lookup.py 53 --json
```

Search by a partial service name:

```bash
python skills/port-service-lookup/scripts/port_service_lookup.py sql
```

The CLI searches a static table of common mappings. It does not scan ports, resolve names, or send network traffic. It returns exit status `1` when a query has no matching mapping.
