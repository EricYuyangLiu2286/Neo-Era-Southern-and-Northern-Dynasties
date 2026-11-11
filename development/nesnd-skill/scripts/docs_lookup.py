"""Look up Victoria 3 script_docs and data-binding records without changing files.

Copied from WORK/tools/vic3_dump_lookup.py (2026-11-05); its test stays at WORK/tools/test_vic3_dump_lookup.py.
Example: python scripts/docs_lookup.py is_on_defending_side --kind trigger
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path


DOCS = {
    "trigger": "triggers", "effect": "effects", "target": "event_targets",
    "saved-target": "event_targets", "on-action": "on_actions",
    "custom-loc": "custom_localization", "modifier": "modifiers",
}
KINDS = (*DOCS, "datatype")
DEFAULT_ROOT = Path(r"D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3")  # user data: docs/ and logs/data_types/
SEPARATOR = re.compile(r"^-{10,}$")


def section_records(lines, pattern):
    """Split by markdown/identifier headings, keeping exact one-based source lines."""
    starts = [(i, match[1]) for i, line in enumerate(lines)
              if (match := pattern.fullmatch(line))]
    for index, (start, name) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(lines)
        yield start, name, lines[start + 1:end]


def separated_records(lines):
    """Return each non-empty block between exact horizontal separators."""
    start = None
    for i, line in enumerate([*lines, "--------------------"]):
        if SEPARATOR.fullmatch(line):
            if start is not None:
                yield start, lines[start], lines[start + 1:i]
            start = None
        elif start is None and line.strip():
            start = i


def fields(body):
    metadata = {}
    for line in body:
        field, colon, value = line.strip().partition(":")
        field = field.strip("*")
        if colon and field in {
            "Supported Scopes", "Supported Targets", "Value Type", "Input Scopes",
            "Output Scopes", "Expected Scope", "Scope", "From Code", "Mask",
            "Definition type", "Return type", "Random Valid", "Requires Data",
        }:
            metadata[field] = value.strip()
    return metadata


def records(path, text):
    # Some engine descriptions contain control characters. Only LF delimits source lines.
    lines = [line.rstrip("\r") for line in text.split("\n")]
    stem = path.stem
    if stem in ("effects", "triggers"):
        entries = section_records(lines, re.compile(r"## (\S+)\s*"))
        kind = "effect" if stem == "effects" else "trigger"
    elif stem == "event_targets":
        split = next((i for i, line in enumerate(lines) if SEPARATOR.fullmatch(line)), len(lines))
        for i, line in enumerate(lines[split:], split):
            if re.fullmatch(r"[\w:-]+", line) and not line.endswith(":"):
                yield {"kind": "saved-target", "name": line, "line": i + 1, "metadata": {}}
        entries = section_records(lines[:split], re.compile(r"### (\S+)\s*"))
        kind = "target"
    elif stem == "modifiers":
        kind = "modifier"
        entries = section_records(lines, re.compile(r"(\S+):"))
    else:
        entries = separated_records(lines)
        kind = {"custom_localization": "custom-loc", "on_actions": "on-action"}.get(stem, "datatype")

    modifier_sections = [(i, s.strip("- ")) for i, s in enumerate(lines)
                         if kind == "modifier" and s.startswith("--- ")]
    for start, header, body in entries:
        metadata = fields(body)
        if kind in ("custom-loc", "on-action") and header.endswith("Documentation:"):
            continue
        name = header.rstrip(":")
        record = {"kind": kind, "name": name, "line": start + 1, "metadata": metadata}
        if kind == "datatype":
            name, _, arg_text = header.partition("(")
            record["name"] = name.strip()
            if arg_text and not arg_text.endswith(")"):
                raise ValueError(f"Unrecognized signature at {path}:{start + 1}: {header}")
            args = [arg.strip() for arg in arg_text.rstrip(")").split(",") if arg.strip()]
            record.update(signature=header, arguments=args, arity=len(args))
            if "." in name:
                record["receiver"] = name.split(".", 1)[0]
        elif kind == "modifier":
            record["section"] = next((s for i, s in reversed(modifier_sections) if i < start), "")
            body = [s for s in body if not s.startswith("--- ")]
        record["body"] = "\n".join(body).strip()
        yield record


def load(root, kind):
    paths = []
    if kind != "datatype":
        paths.extend(root / "docs" / (stem + ".log") for stem in
                     dict.fromkeys([DOCS[kind]] if kind else DOCS.values()))
    if kind in (None, "datatype"):
        data_paths = sorted((root / "logs" / "data_types").glob("data_types_*.txt"))
        if not data_paths:
            raise FileNotFoundError(f"No data_types_*.txt in {root / 'logs' / 'data_types'}")
        paths.extend(data_paths)
    for path in paths:
        raw = path.read_bytes()
        # Invalid bytes in generated prose are printed as \xNN; original files remain untouched.
        decoded = raw.decode("utf-8-sig", "backslashreplace")
        rows = list(records(path, decoded))
        for row in rows:
            row["source"] = str(path)
        yield path, raw, rows


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("name", nargs="?", help="exact exported identifier, including receiver for methods")
    cli.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="user-data or snapshot root containing docs/ and logs/data_types/")
    cli.add_argument("--kind", choices=KINDS)
    cli.add_argument("--prefix", action="store_true", help="match by name prefix")
    cli.add_argument("--scope", help="exact exported input/supported/expected scope, or custom localization scope")
    cli.add_argument("--arity", type=int, help="number of arguments for data-binding records")
    cli.add_argument("--json", action="store_true", help="emit all matching records as JSON")
    cli.add_argument("--inventory", action="store_true", help="show per-file counts and checksums")
    args = cli.parse_args(argv)
    if not args.inventory and not args.name:
        cli.error("specify a name or --inventory")
    results = []
    try:
        for path, raw, rows in load(args.root.resolve(), args.kind):
            if args.kind:
                rows = [r for r in rows if r["kind"] == args.kind]
            if args.inventory:
                invalid = sum(0xdc80 <= ord(c) <= 0xdcff for c in raw.decode("utf-8-sig", "surrogateescape"))
                results.append({"source": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                                "invalid_utf8_bytes": invalid, "counts": dict(collections.Counter(r["kind"] for r in rows))})
                continue
            for r in rows:
                if (not r["name"].startswith(args.name) if args.prefix else r["name"] != args.name):
                    continue
                if args.arity is not None and r.get("arity") != args.arity:
                    continue
                if args.scope and not any(args.scope in [v.strip() for v in r["metadata"].get(f, "").split(",")]
                                          for f in ("Supported Scopes", "Input Scopes", "Expected Scope", "Scope")):
                    continue
                results.append(r)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2
    if args.json or args.inventory:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"{r['kind']} {r.get('signature', r['name'])}  {r['source']}:{r['line']}")
            if "section" in r:
                print(r["section"])
            if r.get("body"):
                print(r["body"])
            print()
    return 0 if results else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    raise SystemExit(main())
