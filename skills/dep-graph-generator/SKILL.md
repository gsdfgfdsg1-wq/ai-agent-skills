---
name: dep-graph-generator
description: Analyze package.json or requirements.txt files and output dependency relationship data as JSON, DOT, or text for visualization and auditing.
license: MIT
---

# Dependency Graph Generator

> Parse package.json or requirements.txt and produce a dependency graph in multiple formats.

## When to Use / Triggers

- Visualize your project's dependency tree before a major upgrade.
- Audit transitive dependency depth and detect diamond dependencies.
- Generate DOT format for Graphviz rendering.
- Security review, identify which packages pull in the most transitive deps.

## Capabilities

- Parses package.json (npm/yarn) and requirements.txt (pip) with version pins.
- Resolves nested package.json dependencies from node_modules (best-effort).
- Outputs JSON (adjacency list), DOT (Graphviz), or indented text.
- `--depth` to limit traversal depth.
- `--format json|dot|text` for output format.

## Usage

```bash
# Text tree from package.json
python skills/dep-graph-generator/scripts/dep_graph.py package.json

# DOT format for Graphviz
python skills/dep-graph-generator/scripts/dep_graph.py package.json --format dot

# From requirements.txt
python skills/dep-graph-generator/scripts/dep_graph.py requirements.txt --format json

# Limit depth
python skills/dep-graph-generator/scripts/dep_graph.py package.json --depth 2
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/dep_graph.py --help` for all options.
