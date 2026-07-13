# Semver Checker — Usage Examples

## 1. Parse a version string

```bash
python skills/semver-checker/scripts/semver.py parse --version "1.2.3-alpha.1+build.123"
```

```
Version: 1.2.3-alpha.1+build.123
  Major:       1
  Minor:       2
  Patch:       3
  Prerelease:  alpha.1
  Build:       build.123
```

## 2. Compare two versions

```bash
python skills/semver-checker/scripts/semver.py compare --left "1.2.3" --right "1.3.0"
```

```
1.2.3 < 1.3.0
```

## 3. Check range satisfaction

```bash
python skills/semver-checker/scripts/semver.py satisfies --version "1.5.0" --range "^1.0.0"
```

```
1.5.0 satisfies ^1.0.0
```

```bash
python skills/semver-checker/scripts/semver.py satisfies --version "2.0.0" --range "^1.0.0"
```

```
2.0.0 does NOT satisfy ^1.0.0
```

## 4. Sort versions

```bash
python skills/semver-checker/scripts/semver.py sort --versions "2.0.0" "1.0.0" "1.5.0" "0.9.0"
```

```
0.9.0
1.0.0
1.5.0
2.0.0
```

## Error handling

Invalid version:

```bash
python skills/semver-checker/scripts/semver.py parse --version "v1.2"
```

```
Error: 'v1.2' is not a valid semver string
```
