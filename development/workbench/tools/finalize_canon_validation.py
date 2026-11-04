"""Bind completed external evidence and independent review to the delivery bytes."""
from canon_routes_context import B, C, M, R, W, PARENT, man, sha, read, dump
from pathlib import Path
import ast
import hashlib
import json
import re

approved = {
    "batch-a-validation.json": "STATIC_PASS",
    "batch-b-validation.json": "STATIC_PASS",
    "batch-c-repair4-validation.json": "STATIC_PASS_C1_WITH_EXPLICIT_DEPENDENCY_AND_WARNINGS",
    "batch-a2-repair3-validation.json": "EXTERNAL_SOURCE_PASS_ENGINE_NOT_RUN",
    "batch-b2-repair2-validation.json": "PASS_EXTERNAL_SOURCE_MATRIX_ENGINE_NOT_RUN",
    "batch-c2-repair3-validation.json": "STATIC_PASS",
    "final-button-preview-repair1-validation.json": "STATIC_PASS",
    "final-writing-independent-review-r2.json": "EDITORIAL_SOURCE_PASS",
}
evidence = {}
for name, expected in approved.items():
    data = json.loads(read(R / name))
    assert data["status"] == expected, (name, data["status"])
    evidence[name] = {"status": expected, "sha256": sha(R / name)}
ui = json.loads(read(R / "final-button-preview-repair1-validation.json"))
uf = json.loads(read(R / "final-button-preview-repair1-freeze.json"))
assert ui["freeze_manifest_sha256"] == sha(R / "final-button-preview-repair1-freeze.json")
assert not ui["findings"]
editorial = json.loads(read(R / "final-writing-independent-review-r2.json"))
assert not editorial["findings"]
for relative, expected in editorial["four_text_sha256"].items():
    # The review may use an absolute path or a candidate-relative path.
    path = Path(relative)
    if not path.is_absolute():
        path = C / relative
    assert sha(path) == expected, relative
cm, bm, mm = man(C), man(B), man(M)
assert cm == uf["full_snapshot_files"], "Candidate changed after final external tests"
assert not bm.keys() - cm.keys(), "Unreviewed deletions"
patch = {relative: value for relative, value in cm.items()
         if bm.get(relative) != value}
conflicts = [relative for relative, value in patch.items()
             if mm.get(relative) not in (bm.get(relative), value)]
assert not conflicts, conflicts

tool_names = {
    "canon_routes_context.py", "qin_persia_context.py",
    "deliver_canon_routes.py", "finalize_canon_validation.py",
    "prepare_canon_final_review.py", "snapshot_canon_integration.py",
}
prefix = str(W / "tools").replace("\\", "/")
pattern = re.compile(re.escape(prefix) + r"/([A-Za-z0-9_.-]+\.py)\b")
def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)

for report in R.rglob("*.json"):
    if report.stat().st_size > 3_000_000:
        continue
    try:
        data = json.loads(read(report))
    except (ValueError, UnicodeError):
        continue
    for value in strings(data):
        for name in pattern.findall(value.replace("\\", "/")):
            if (W / "tools" / name).is_file():
                tool_names.add(name)

# Later validators record relative tool names in Markdown as well as JSON.
# Preserve those real test programs and their local imports with the evidence.
for report in R.rglob("*"):
    if (report.is_file() and report.suffix in {".md", ".json"}
            and report.stat().st_size <= 3_000_000):
        for name in re.findall(r"\b([A-Za-z0-9_][A-Za-z0-9_.-]*\.py)\b", read(report)):
            if (W / "tools" / name).is_file():
                tool_names.add(name)
pending = list(tool_names)
while pending:
    name = pending.pop()
    module = ast.parse(read(W / "tools" / name))
    for node in ast.walk(module):
        modules = ([node.module] if isinstance(node, ast.ImportFrom) and node.module
                   else [a.name for a in node.names] if isinstance(node, ast.Import)
                   else [])
        for imported in modules:
            dependency = imported.split(".")[0] + ".py"
            if dependency not in tool_names and (W / "tools" / dependency).is_file():
                tool_names.add(dependency)
                pending.append(dependency)

result = {
    "status": "STATIC_PASS",
    "engine_verified": False,
    "required_batches_complete": True,
    "parent": PARENT,
    "candidate": str(C),
    "baseline": str(B),
    "game_version": "1.13.11",
    "build": "24799966",
    "source_files": cm,
    "mod_sha256": hashlib.sha256(
        json.dumps(cm, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    "changed_files": len(patch),
    "gameplay_changed_files": sum(not p.startswith(("docs/", ".scratch/"))
                                  for p in patch),
    "deletions": [],
    "reviews_remaining": {"standards": 0, "spec": 0},
    "review_closure": {
        "standards_original": "final-standards-review.json",
        "spec_original": "final-spec-review.json",
        "independent_editorial_closure": "final-writing-independent-review-r2.json",
        "display_closure": "final-button-preview-repair1-validation.json",
    },
    "evidence": evidence,
    "integration_notes": [
        "C1 kind5 dependency and dormant JE localization warnings closed by later B2/C2 evidence",
        "Final UI tests bind the whole 1015-file source and preserve real effects and original values",
        "Old failed tests, harness false positives and superseded freezes are retained",
    ],
    "known_tool_diagnostics": [
        "Native control_half_target_country_states enum is missing in Tiger schema",
        "Saved original HUS scope forwarding is path-sensitive; full caller/source checked",
        "Inherited native opium article scope and nonfunctional formatting/logic warnings are classified in batch reports",
    ],
    "limits": [
        "No Victoria 3 launch or engine validation in this task",
        "Native scheduling, UI rendering, save/load and natural AI/economic outcomes remain unverified",
        "Source AST fixtures execute source control flow but explicitly adapt native operations",
        "Historical population and starting treaty/law changes primarily apply to new games",
        "Earlier separately queued France development, Gujarat/fleet and editor work remain recorded outside task34",
    ],
    "delivery_tool_files": sorted(tool_names),
}
dump(R / "patch-files.json", patch)
dump(R / "final-validation.json", result)
print(json.dumps({"status": result["status"], "files": len(cm),
                  "changed": len(patch), "tools": len(tool_names),
                  "engine_verified": False}))
