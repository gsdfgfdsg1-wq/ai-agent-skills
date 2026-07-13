# Usage Examples

## 1. Calculate a standard subnet

```bash
python skills/netmask-calculator/scripts/netmask_calculator.py 192.168.1.10/24
```

```text
CIDR:              192.168.1.0/24
Network address:   192.168.1.0
Broadcast address: 192.168.1.255
Netmask:           255.255.255.0 (/24)
Hostmask:          0.0.0.255
Total addresses:   256
Usable hosts:      254
Host range:        192.168.1.1 - 192.168.1.254
```

## 2. Emit JSON

```bash
python skills/netmask-calculator/scripts/netmask_calculator.py 10.20.30.40/16 --json
```

## 3. Inspect a point-to-point subnet

```bash
python skills/netmask-calculator/scripts/netmask_calculator.py 203.0.113.0/31
```

## 4. Inspect a single-host route

```bash
python skills/netmask-calculator/scripts/netmask_calculator.py 203.0.113.9/32
```
