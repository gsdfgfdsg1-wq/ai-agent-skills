# Usage Examples

## 1. Text tree from package.json

```bash
python skills/dep-graph-generator/scripts/dep_graph.py package.json
```

Output:

```text
my-app
  - axios
  - express
    - body-parser
    - cookie
  - lodash
```

## 2. DOT format for Graphviz

```bash
python skills/dep-graph-generator/scripts/dep_graph.py package.json --format dot > deps.dot
dot -Tpng deps.dot -o deps.png
```

## 3. JSON adjacency list

```bash
python skills/dep-graph-generator/scripts/dep_graph.py package.json --format json
```

Returns `{"root": "my-app", "graph": {"my-app": ["axios", "express", "lodash"], ...}}`.

## 4. From requirements.txt

```bash
python skills/dep-graph-generator/scripts/dep_graph.py requirements.txt --format text
```

## 5. Limit depth

```bash
python skills/dep-graph-generator/scripts/dep_graph.py package.json --depth 1
```

Only shows direct dependencies, no transitive resolution.
