# JSONL Deduper Examples

Deduplicate by a top-level identifier, keeping the first record:

```bash
python scripts/dedupe_jsonl.py events.jsonl events.unique.jsonl --key event_id --keep first --stats-json events.stats.json
```

Deduplicate by a nested key and keep the last occurrence:

```bash
python scripts/dedupe_jsonl.py customers.jsonl customers.unique.jsonl --key customer.email --keep last
```

Given this input:

```jsonl
{"event_id":"e-1","status":"pending"}
{"event_id":"e-2","status":"open"}
{"event_id":"e-1","status":"completed"}
```

`--keep first` writes the first two records. `--keep last` writes `e-2` followed by the completed `e-1` record, preserving the order of the retained source positions.

Both standard output and the optional `--stats-json` file contain JSON like:

```json
{
  "input_records": 3,
  "output_records": 2,
  "duplicates_removed": 1,
  "key": "event_id",
  "keep": "first"
}
```

A malformed JSON line, a non-object record, or a missing dotted key stops processing with exit code `2` and leaves the requested output file untouched.
