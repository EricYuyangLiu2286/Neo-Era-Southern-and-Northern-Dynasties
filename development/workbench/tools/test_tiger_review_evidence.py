"""Evidence matching regressions; fixtures stay outside candidate and GAME."""
from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import json
import unittest

from classify_tiger_reviews import diagnostic_signature, file_sha, match_review

W = Path("D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench")


class EvidenceBinding(unittest.TestCase):
    def setUp(self):
        fixture_root = W / "qa-fixtures"
        fixture_root.mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(prefix="tiger-review-", dir=fixture_root)
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(fixture_root.resolve())
        self.source = self.root / "case.txt"
        self.source.write_text("enum = native_supported\n")
        self.proof = self.root / "proof.json"
        self.proof.write_text('{"review": "specific source comparison"}\n')
        self.diag = {"key": "choice", "severity": "error", "message": "unsupported enum",
                     "locations": [{"path": "case.txt", "from": "MOD", "line": "enum = native_supported",
                                    "fullpath": str(self.source), "linenr": 1}]}
        self.record = {
            "diagnostic_sha256": diagnostic_signature(self.diag),
            "classification": "EXACT_TOOL_GAP", "disposition": "tool_gap",
            "assessment": "Only this exact source and diagnostic.",
            "source_witnesses": [{"relative": "case.txt", "sha256": file_sha(self.source)}],
            "evidence": {"path": str(self.proof), "sha256": file_sha(self.proof)},
        }
        self.register = {"tiger_reviews": [self.record]}

    def tearDown(self):
        self.temp.cleanup()

    def test_exact_match_is_only_static(self):
        result = match_review(self.diag, self.root, self.register)
        self.assertFalse(result["requires_resolution"])
        self.assertFalse(result["engine_verified"])

    def test_same_key_different_token_is_not_waived(self):
        changed = copy.deepcopy(self.diag)
        changed["locations"][0]["line"] = "enum = invented"
        self.assertIsNone(match_review(changed, self.root, self.register))

    def test_source_drift_invalidates_review(self):
        self.source.write_text("enum = changed\n")
        self.assertIsNone(match_review(self.diag, self.root, self.register))

    def test_proof_drift_invalidates_review(self):
        self.proof.write_text('{"review": "changed"}\n')
        self.assertIsNone(match_review(self.diag, self.root, self.register))

    def test_missing_proof_invalidates_review(self):
        self.proof.unlink()
        self.assertIsNone(match_review(self.diag, self.root, self.register))

    def test_runtime_question_stays_unresolved(self):
        self.record["disposition"] = "requires_engine_review"
        self.assertTrue(match_review(self.diag, self.root, self.register)["requires_resolution"])

    def test_inherited_defect_stays_unresolved(self):
        self.record["disposition"] = "confirmed_inherited_defect"
        self.assertTrue(match_review(self.diag, self.root, self.register)["requires_resolution"])

    def test_witnesses_required(self):
        self.record["source_witnesses"] = []
        self.assertIsNone(match_review(self.diag, self.root, self.register))

    def test_line_relocation_retains_source_binding(self):
        changed = copy.deepcopy(self.diag)
        changed["locations"][0]["linenr"] = 20
        changed["locations"][0]["fullpath"] = "another-frozen-root/case.txt"
        self.assertIsNotNone(match_review(changed, self.root, self.register))


class CurrentReports(unittest.TestCase):
    def test_actual_clone_and_russia_diagnostics_have_different_dispositions(self):
        candidate = W / "exports/batch-debug-20261101-f2"
        register = json.loads((W / "validation/review-register-f2.json").read_text(encoding="utf-8"))
        diagnostics = json.loads((W / "validation/runs/f1-global-20261101-final/tiger_raw.json").read_text(encoding="utf-8"))
        clone, russia = [], []
        cache = {}
        for diagnostic in diagnostics:
            result = match_review(diagnostic, candidate, register, cache)
            if result and result["classification"] == "CURRENT_NATIVE_ANNEX_CLONE_TOOL_GAP":
                clone.append(result)
            if result and result["classification"] == "CURRENT_GAME_INHERITED_EMPTY_IF":
                russia.append(result)
        self.assertEqual(len(clone), 5)
        self.assertEqual(len(russia), 1)
        self.assertTrue(all(not r["requires_resolution"] for r in clone))
        self.assertTrue(russia[0]["requires_resolution"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
