"""Prepare an immutable snapshot diff for two independent review axes."""
from canon_routes_context import B, C, M, R, W, PARENT, man, read, dump
from pathlib import Path
from datetime import datetime, timezone
import difflib
import shutil
import subprocess

repo = W / "projects/nesnd-repository"
assert subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip() == PARENT
assert not subprocess.check_output(
    ["git", "status", "--porcelain"], cwd=repo, text=True).strip()
bm, cm, mm = man(B), man(C), man(M)
assert not bm.keys() - cm.keys(), "Deletion needs separate review"
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
frozen = W / "validation/snapshots" / ("canon-final-review-" + stamp) / "mod"
assert not frozen.exists()
shutil.copytree(C, frozen)
assert man(C) == cm == man(frozen)
changes = {p: {"before": bm.get(p), "after": h}
           for p, h in cm.items() if bm.get(p) != h}
conflicts = [p for p, h in changes.items()
             if mm.get(p) != h["before"] and mm.get(p) != h["after"]]
diff_path = R / "final-review.diff"
with diff_path.open("w", encoding="utf-8", newline="") as output:
    for relative in sorted(changes):
        old_path, new_path = B / relative, frozen / relative
        try:
            old = old_path.read_text("utf-8-sig") if old_path.exists() else ""
            new = new_path.read_text("utf-8-sig")
        except UnicodeDecodeError:
            output.write("Binary change: " + relative + "\n")
            continue
        output.writelines(difflib.unified_diff(
            old.splitlines(keepends=True), new.splitlines(keepends=True),
            fromfile="baseline/" + relative, tofile="candidate/" + relative))
contract = {
    "parent": PARENT, "baseline": str(B), "candidate_source": str(C),
    "frozen": str(frozen), "source_files": cm, "baseline_files": bm,
    "changes": changes, "changed_files": len(changes),
    "deletions": [], "main_concurrent_conflicts": conflicts,
    "snapshot_review_not_git_head_diff": True,
    "diff_command": "python -X utf8 " + str(Path(__file__)),
    "diff": str(diff_path), "created_utc": stamp,
    "engine_verified": False,
}
dump(R / "final-review-contract.json", contract)
dump(frozen.parent / "manifest.json", contract)
print(str(frozen))
print("Changed files:", len(changes), "Conflicts:", len(conflicts))
