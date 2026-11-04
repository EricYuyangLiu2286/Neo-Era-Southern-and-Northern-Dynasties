"""Deliver a separately reviewed and frozen candidate. Dry-run by default."""
from canon_routes_context import B, C, M, R, W, S, PARENT, man, sha, read, dump
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

def checked_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(("Outside delivery root", root, relative))
    return path

def git(repo, *args):
    return subprocess.check_output(
        ["git", *args], cwd=repo, text=True, encoding="utf-8"
    ).strip()

def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    if sha(source) != sha(target):
        raise RuntimeError(("Copy verification failed", source, target))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backup", type=Path, required=True,
                    help="Verified final candidate backup MOD root")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    final = json.loads(read(R / "final-validation.json"))
    if final["status"] != "STATIC_PASS" or final["engine_verified"] is not False:
        raise RuntimeError("This delivery requires the actual external-only result")
    if final["reviews_remaining"] != {"standards": 0, "spec": 0}:
        raise RuntimeError("Reviews are not closed")
    if final["required_batches_complete"] is not True:
        raise RuntimeError("An authorized batch remains unfinished")
    bm, cm, mm = man(B), man(C), man(M)
    if cm != final["source_files"] or man(args.backup) != cm:
        raise RuntimeError("Candidate changed after verification or backup differs")
    if bm.keys() - cm.keys():
        raise RuntimeError("Unreviewed source deletion")
    patch = {rel: h for rel, h in cm.items() if bm.get(rel) != h}
    conflicts = [rel for rel, h in patch.items()
                 if mm.get(rel) != bm.get(rel) and mm.get(rel) != h]
    if conflicts:
        dump(R / "merge-conflicts.json", {"conflicts": conflicts})
        raise RuntimeError("Concurrent edits require a reviewed three-way merge")
    expected = dict(mm)
    expected.update(patch)
    concurrent = {rel: h for rel, h in mm.items()
                  if bm.get(rel) != h and rel not in patch}
    repo = W / "projects/nesnd-repository"
    if git(repo, "rev-parse", "HEAD") != PARENT:
        raise RuntimeError("Repository parent changed; review before delivery")
    if git(repo, "status", "--porcelain"):
        raise RuntimeError("Uncommitted repository work must be preserved")
    if git(repo, "branch", "--show-current") != "main":
        raise RuntimeError("Unexpected repository branch")
    for rel, h in bm.items():
        path = checked_path(repo, rel)
        if not path.is_file() or sha(path) != h:
            raise RuntimeError(("Repository baseline differs", rel))
    for rel in patch:
        checked_path(M, rel)
        checked_path(repo, rel)
    readiness = {
        "candidate": str(C), "parent": PARENT, "changed": patch,
        "preserved_concurrent_files": concurrent, "deletions": [],
        "verified_backup": str(args.backup), "apply_requested": args.apply,
    }
    dump(R / "delivery-readiness.json", readiness)
    if not args.apply:
        print(json.dumps({"ready": True, "changed_files": len(patch),
                          "preserved_concurrent_files": len(concurrent)}))
        return

    # A fresh full target backup precedes any deployment mutation.
    subprocess.run([
        sys.executable, "-X", "utf8", str(S / "scripts/backup.py"),
        "--source", str(M), "--label", "canon-routes-deployment",
        "--status", "pre-change"
    ], check=True)
    if man(M) != mm or man(C) != cm:
        raise RuntimeError("Source or main changed while backing up")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    branch = "feature/canon-routes-" + stamp
    subprocess.run(["git", "switch", "-c", branch], cwd=repo, check=True)
    for rel, h in patch.items():
        destination = checked_path(M, rel)
        current = sha(destination) if destination.is_file() else None
        if current != mm.get(rel):
            raise RuntimeError(("Concurrent target edit during deployment", rel))
        copy_file(checked_path(C, rel), destination)
    if man(M) != expected:
        raise RuntimeError("Main deployment does not match the reviewed merge")
    dump(R / "main-merge.json", {
        **readiness, "branch": branch, "main": expected,
        "engine_verified": False, "merged_at_utc": stamp
    })
    for rel, h in expected.items():
        destination = checked_path(repo, rel)
        if not destination.is_file() or sha(destination) != h:
            copy_file(checked_path(M, rel), destination)

    # Skills and development evidence belong in source control, not the game ZIP.
    for source, destination in [
        (S, repo / "development/nesnd-skill"),
        (S.parent / "nesnd-player-writing", repo / "development/nesnd-player-writing"),
    ]:
        for item in source.rglob("*"):
            if item.is_file() and item.suffix in {".md", ".yaml", ".py"}:
                copy_file(item, destination / item.relative_to(source))
    for item in (W / "plans/two-empires").glob("*.md"):
        copy_file(item, repo / "development/workbench/plans/two-empires" / item.name)
    for item in R.rglob("*"):
        if (item.is_file() and item.suffix in {".md", ".json", ".diff"}
                and item.stat().st_size <= 3_000_000):
            copy_file(item, repo / "development/workbench/reports" /
                      R.name / item.relative_to(R))
    for name in final["delivery_tool_files"]:
        source = checked_path(W / "tools", name)
        copy_file(source, checked_path(repo / "development/workbench/tools", name))

    package = W / "releases" / ("nesnd-canon-routes-" + stamp + ".zip")
    package.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package, "x", zipfile.ZIP_DEFLATED) as z:
        for rel in expected:
            if rel.startswith(("docs/", ".scratch/", "development/", "tools/")):
                continue
            if rel.endswith((".md", ".bak", ".py", ".pyc")):
                continue
            if any(q in rel for q in
                   ("nesnd_qa", "nesnd_f2_qa", "nesnd_batch_probe", "nesnd_sequence_qa")):
                raise RuntimeError(("QA file in release", rel))
            z.write(checked_path(M, rel), rel)
    with zipfile.ZipFile(package) as z:
        for rel in z.namelist():
            if hashlib.sha256(z.read(rel)).hexdigest() != expected[rel]:
                raise RuntimeError(("Package mismatch", rel))
    dump(R / "package.json", {
        "path": str(package), "sha256": sha(package),
        "matches_main": True, "QA_included": False, "engine_verified": False
    })
    copy_file(R / "package.json", repo / "development/workbench/reports" /
              R.name / "package.json")
    subprocess.run(["git", "add", "--all"], cwd=repo, check=True)
    check = subprocess.run([
        "git", "-c",
        "core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof",
        "diff", "--cached", "--check", "--", ".",
        ":(exclude)development/workbench/reports/**"
    ], cwd=repo, text=True, encoding="utf-8", capture_output=True)
    dump(R / "git-whitespace.json",
         {"status": check.returncode, "output": check.stdout + check.stderr})
    if check.returncode:
        raise RuntimeError("Review staged whitespace errors; no automatic rewrite")
    if man(M) != expected:
        raise RuntimeError("Main changed before source commit")
    print(json.dumps({"deployed": True, "branch": branch,
                      "package": str(package), "commit_pending": True}))

if __name__ == "__main__":
    main()
