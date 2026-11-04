"""Freeze all stopped candidate edits together; this is not an acceptance test."""
from canon_routes_context import C, R, W, man, dump
from datetime import datetime, timezone
import shutil

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
target = W / "validation/snapshots" / ("canon-integration-" + stamp) / "mod"
assert target.resolve().is_relative_to((W / "validation/snapshots").resolve())
assert not target.exists()
before = man(C)
shutil.copytree(C, target)
assert man(C) == before == man(target), "Source changed while freezing"
report = {
    "snapshot": str(target), "source": str(C), "source_files": before,
    "files": len(before), "created_utc": stamp,
    "status": "FROZEN_NOT_ACCEPTED", "engine_verified": False,
    "batches": ["A1", "B1-r3", "C1-repair4", "A2-repair2", "B2-repair1", "C2-final-155623"],
    "known_pending": ["C2 confirmed red cases require repair", "A2 and B2 complete retests pending"],
}
dump(target.parent / "manifest.json", report)
dump(R / "integration-snapshot-current.json", report)
print(str(target))
