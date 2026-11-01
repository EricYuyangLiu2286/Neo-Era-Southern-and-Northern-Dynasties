"""Match explicitly reviewed Tiger diagnostics to unchanged source and evidence.

A match records a review, not engine execution. Only exact tool-rule gaps or
format-only findings are nonblocking; inherited defects and runtime questions
remain unresolved. No diagnostic family is globally ignored.
"""
from pathlib import Path
import hashlib
import json


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def diagnostic_signature(diagnostic):
    """Keep diagnostic text and source lines; omit machine path and positions."""
    value = {k: v for k, v in diagnostic.items() if k != "locations"}
    value["locations"] = [
        {k: v for k, v in location.items()
         if k not in {"fullpath", "linenr", "column", "length"}}
        for location in (diagnostic.get("locations") or [])
    ]
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def match_review(diagnostic, candidate, register, hash_cache=None):
    def current_sha(path):
        key = str(path)
        if hash_cache is None:
            return file_sha(path)
        if key not in hash_cache:
            hash_cache[key] = file_sha(path)
        return hash_cache[key]

    signature = diagnostic_signature(diagnostic)
    for review in register.get("tiger_reviews", []):
        if review.get("diagnostic_sha256") != signature:
            continue
        witnesses = review.get("source_witnesses", [])
        if not witnesses:
            continue
        valid = True
        for witness in witnesses:
            path = (Path(candidate) / witness["relative"]
                    if "relative" in witness else Path(witness["path"]))
            if not path.is_file() or current_sha(path) != witness.get("sha256"):
                valid = False
                break
        evidence = review.get("evidence", {})
        proof = Path(evidence.get("path", ""))
        if (not valid or not proof.is_file()
                or current_sha(proof) != evidence.get("sha256")):
            continue
        disposition = review.get("disposition", "requires_review")
        return {
            "classification": review["classification"],
            "disposition": disposition,
            "requires_resolution": disposition not in {"tool_gap", "format_only"},
            "evidence": evidence,
            "source_witnesses": witnesses,
            "assessment": review["assessment"],
            "diagnostic_sha256": signature,
            "engine_verified": False,
        }
    return None
