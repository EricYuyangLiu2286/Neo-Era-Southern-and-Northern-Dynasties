"""Build the explicitly reviewed F2 register, preserving the earlier register."""
from pathlib import Path
import sys
import json

W = Path("D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench")
G = Path("D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game")
C = W / "exports/batch-debug-20261101-f2"
OUT = W / "validation/f2-review"
sys.path.insert(0, "C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts")
from pdx import read, unquote
from classify_tiger_reviews import diagnostic_signature, file_sha


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_new(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)


def shape(node):
    return (node.key, node.value, node.op, node.prefix,
            None if node.children is None else tuple(shape(n) for n in node.children))


raw = read_json(W / "validation/runs/f1-global-20261101-final/tiger_raw.json")
old_raw = read_json(W / "validation/runs/e1-global-20261031-b/tiger_raw.json")
old_proof = W / "plans/two-empires/evidence/tiger-e1-eac-exact-source-review.json"
prior = read_json(old_proof)
for path, expected in prior["source_witness_sha256"].items():
    assert file_sha(path) == expected, f"Stale review source: {path}"
old_map = {diagnostic_signature(old_raw[r["index"]]): r for r in prior["records"]}
register = read_json(W / "validation/review-register.json")
register["revision"] = "F2 source review 2026-11-01; runtime remains separate"
register["prior_register"] = {
    "path": str(W / "validation/review-register.json"),
    "sha256": file_sha(W / "validation/review-register.json"),
}
reviews, skipped, seen = [], [], set()
proof_sources = [{"path": p, "sha256": h} for p, h in prior["source_witness_sha256"].items()]
for diagnostic in raw:
    sig = diagnostic_signature(diagnostic)
    old_record = old_map.get(sig)
    if not old_record or sig in seen:
        continue
    witnesses, valid = [], True
    for location in diagnostic.get("locations") or []:
        relative = (location.get("path") or "").replace("\\", "/")
        if not relative:
            continue
        if location.get("from") == "MOD":
            path = C / relative
            expected = prior["candidate_manifest"].get(relative)
            if not expected or not path.is_file() or file_sha(path) != expected:
                valid = False
                break
            witnesses.append({"relative": relative, "sha256": expected})
        elif location.get("fullpath"):
            path = Path(location["fullpath"])
            if not path.is_file():
                valid = False
                break
            witnesses.append({"path": str(path), "sha256": file_sha(path)})
    if not valid or not witnesses:
        skipped.append({"diagnostic_sha256": sig, "classification": old_record["classification"],
                        "reason": "Diagnostic source changed or no verifiable witness"})
        continue
    classification = old_record["classification"]
    disposition = "requires_engine_review"
    if classification in {
        "CURRENT_GAME_API_SUPPORTED", "ENGINE_API_AND_NATIVE_VALUE_SUPPORTED",
        "CURRENT_ENGINE_SCOPE_RULE_SUPPORTED",
    }:
        disposition = "tool_gap"
    elif classification == "STYLE_OR_NONFUNCTIONAL_SIMPLIFICATION":
        disposition = "format_only"
    elif classification == "CURRENT_GAME_INHERITED_EMPTY_IF":
        disposition = "confirmed_inherited_defect"
    elif classification in {
        "CANDIDATE_LITERAL_UI_LOCALIZATION_GAP", "DEPENDENCY_DEBUG_LOCALIZATION_MISSING",
        "ENGINE_MODIFIER_LOCALIZATION_GAP",
    }:
        disposition = "source_review_required"
    reviews.append({
        "diagnostic_sha256": sig, "classification": classification,
        "disposition": disposition, "assessment": old_record["assessment"],
        "source_witnesses": witnesses + proof_sources,
        "evidence": {"path": str(old_proof), "sha256": file_sha(old_proof)},
        "review_reused_only_for_unchanged_sources": True,
    })
    seen.add(sig)

_, new_tree = read(C / "common/war_goal_types/nesnd_usm_annex.txt")
_, native_tree = read(G / "common/war_goal_types/00_annex_country.txt")
cloned = new_tree.children[0]
native = next(n for n in native_tree.children if n.key == "annex_country")
assert all(not n.children for n in native.all("on_enforced")), "Native callback is no longer empty"
assert tuple(shape(n) for n in cloned.children if n.key != "on_enforced") == tuple(
    shape(n) for n in native.children if n.key != "on_enforced"
), "War-goal body differs beyond the reviewed callback"
_, polish_tree = read(C / "events/ce_poland_events.txt")
assert all(n.key is not None for n in polish_tree.children)
route_refs = {k: [] for k in ["usm_civilwar.4", "usm_civilwar.20", "usm_civilwar.25"]}
script_files = sorted(p for directory in ["common", "events"] for p in (C / directory).rglob("*.txt"))
parse_failures = []
for path in script_files:
    try:
        text, tree = read(path)
    except ValueError as error:
        parse_failures.append({"relative": path.relative_to(C).as_posix(), "error": str(error)})
        continue
    for node in tree.walk():
        value = unquote(node.value)
        if value in route_refs:
            route_refs[value].append({"relative": path.relative_to(C).as_posix(),
                                     "line": text.count("\n", 0, node.start) + 1})
assert not parse_failures, parse_failures
assert not route_refs["usm_civilwar.4"] and not route_refs["usm_civilwar.20"]
assert route_refs["usm_civilwar.25"]
proof = OUT / "source-review.json"
write_new(proof, {
    "candidate": str(C), "engine_verified": False, "game_version": "1.13.11", "game_build": "24799966",
    "native_annex_clone_ordered_ast_equal_without_callbacks": True,
    "native_callback_empty": True,
    "clone_sha256": file_sha(C / "common/war_goal_types/nesnd_usm_annex.txt"),
    "native_annex_sha256": file_sha(G / "common/war_goal_types/00_annex_country.txt"),
    "polish_event_top_level_keys": [n.key for n in polish_tree.children],
    "polish_event_sha256": file_sha(C / "events/ce_poland_events.txt"),
    "route_literal_references": route_refs, "parsed_script_files": len(script_files),
    "boundary": "Static routing, exact source equivalence and parser balance only; callbacks, previews and game-over need native runs.",
    "reused_review_signatures": len(reviews), "skipped_source_drift_records": skipped,
})
for diagnostic in raw:
    paths = {(loc.get("path") or "").replace("\\", "/") for loc in diagnostic.get("locations") or []}
    sig = diagnostic_signature(diagnostic)
    if sig in seen:
        continue
    if "common/war_goal_types/nesnd_usm_annex.txt" in paths and diagnostic.get("key") in {"choice", "scopes"}:
        reviews.append({
            "diagnostic_sha256": sig, "classification": "CURRENT_NATIVE_ANNEX_CLONE_TOOL_GAP",
            "disposition": "tool_gap",
            "assessment": "The complete ordered body equals current GAME annex_country after excluding callbacks; the native callback is empty. Retain native enum, target_region, costs and mirrors. Added callback runtime is unverified.",
            "source_witnesses": [
                {"relative": "common/war_goal_types/nesnd_usm_annex.txt", "sha256": file_sha(C / "common/war_goal_types/nesnd_usm_annex.txt")},
                {"path": str(G / "common/war_goal_types/00_annex_country.txt"), "sha256": file_sha(G / "common/war_goal_types/00_annex_country.txt")},
            ], "evidence": {"path": str(proof), "sha256": file_sha(proof)},
        })
        seen.add(sig)
    elif "events/ce_poland_events.txt" in paths and diagnostic.get("key") == "brace-placement":
        reviews.append({
            "diagnostic_sha256": sig, "classification": "EXACT_POLISH_FORMAT_REVIEW",
            "disposition": "format_only",
            "assessment": "This complete event file parses with balanced blocks and named top-level definitions. The exact closing-brace indentation warning is not a missing-brace parse failure; gameplay still needs engine tests.",
            "source_witnesses": [{"relative": "events/ce_poland_events.txt", "sha256": file_sha(C / "events/ce_poland_events.txt")}],
            "evidence": {"path": str(proof), "sha256": file_sha(proof)},
        })
        seen.add(sig)
register["tiger_reviews"] = reviews
reasons = {
    "south_settlement_overseas_annexation": "JAP annexation is an accepted intermediate outcome. F1 recovery hooks are implemented; non-JAP overseas outcomes and actual restoration/data conservation remain unverified.",
    "civilwar_native_wargoal_annexation": "Native annex semantics are retained with a scoped callback and registered old-target hook. Defeated target lifetime, surrender, victory and 1-day delivery need engine verification.",
    "lin_defection_regression": "Original YN1 pro-Ming transfer and .25 notice are restored with same-character guards. Actual option, negative cases and timing remain unverified.",
    "loser_player_continuation": "Confirmed source gap: old .4 defeat/player-continuation event has zero literal callers; .8 immediately annexes defeated participants. No replacement player-choice entry was implemented. Native game-over consequences need tests.",
    "japan_result_routes": "Old .20 sovereignty-choice route has zero literal callers; existing .41 modifier choices are not an equivalent sovereignty/notification route. This original-route gap remains unresolved; new narrative is not authorized.",
}
all_witnesses = [{"relative": p.relative_to(C).as_posix(), "sha256": file_sha(p)} for p in script_files]
for item in register["manual_checks"]:
    key = item["id"]
    item["previous_review"] = {k: item[k] for k in ["status", "reason", "source_witnesses", "evidence"]}
    item["status"] = "FAIL" if key in {"loser_player_continuation", "japan_result_routes"} else "NOT_RUN"
    item["reason"] = reasons[key]
    item["source_review_completed"] = True
    item["engine_verified"] = False
    item["implementation_status"] = "unresolved" if item["status"] == "FAIL" else "implemented_pending_engine"
    item["source_witnesses"] = all_witnesses
    item["evidence"] = {"path": str(proof), "sha256": file_sha(proof)}
register_path = W / "validation/review-register-f2.json"
write_new(register_path, register)
print(json.dumps({"register": str(register_path), "reviewed_signatures": len(reviews),
                  "scope_drift_skips": len(skipped), "source_review": str(proof),
                  "route_refs": route_refs}, ensure_ascii=False))
