"""Regression tests for the 1.15 engine dump reader. Run with python -B this_file.py."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import vic3_dump_lookup as lookup


class EngineDumpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.by_name = {}
        for path, raw, records in lookup.load(lookup.DEFAULT_ROOT, None):
            for record in records:
                cls.by_name.setdefault((record["kind"], record["name"]), []).append(record)

    def call(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = lookup.main(["--json", *args])
        return code, json.loads(output.getvalue())

    def test_country_name_getters_have_receiver_return_and_zero_arguments(self):
        for name in ("GetName", "GetNameNoFlag", "GetNameDef", "GetNameNoFormatting", "GetAdjective"):
            r, = self.by_name["datatype", "Country." + name]
            self.assertEqual((r["receiver"], r["arity"], r["metadata"]["Return type"]), ("Country", 0, "CString"))

    def test_overloads_survive_without_inventing_argument_types(self):
        rows = self.by_name["datatype", "TopScope.sCountry"]
        self.assertEqual({(r["metadata"]["Definition type"], r["metadata"]["Return type"]) for r in rows},
                         {("Promote", "Country"), ("Function", "[unregistered]")})
        self.assertTrue(all(r["arguments"] == ["Arg0"] for r in rows))
        self.assertEqual(self.call("TopScope.sCountry", "--kind", "datatype", "--arity", "2"), (1, []))

    def test_scope_input_output_distinction_and_source_line(self):
        code, rows = self.call("owner", "--kind", "target", "--scope", "state")
        self.assertEqual(code, 0)
        self.assertEqual(rows[0]["metadata"]["Output Scopes"], "country")
        for row in rows:
            path = Path(row["source"])
            self.assertEqual(path.read_text(encoding="utf-8-sig").split("\n")[row["line"]-1].strip(), "### owner")
        self.assertEqual(self.call("owner", "--kind", "target", "--scope", "state_region"), (1, []))

    def test_native_hub_inputs_and_invalid_utf8_preserve_neighboring_fields(self):
        r, = self.by_name["effect", "set_hub_names"]
        self.assertEqual(r["metadata"]["Supported Scopes"], "state")
        r, = self.by_name["effect", "every_country_in_afghanistan"]
        self.assertIn(r"\x", r["body"])
        self.assertEqual(r["metadata"]["Supported Targets"], "country")
        r, = self.by_name["trigger", "has_law_or_variant"]
        self.assertIn("country", r["metadata"]["Supported Scopes"])

    def test_mod_scope_custom_key_and_code_saved_targets(self):
        action, = self.by_name["on-action", "REPLACE:ryukyu_rivalry_coin_toss"]
        self.assertIn("Expected Scope", action["metadata"])
        loc, = self.by_name["custom-loc", "great_game_victory_caucasus"]
        self.assertEqual(loc["metadata"]["Scope"], "country")
        self.assertIn("gg_caucasian_war_blank", loc["body"])
        modifier, = self.by_name["modifier", "building_angkor_wat_throughput_add"]
        self.assertEqual(modifier["metadata"]["Mask"], "building")
        self.assertEqual(modifier["section"], "Potential dynamic modifier types")
        self.assertIn(("saved-target", "context"), self.by_name)
        self.assertNotIn("Event Targets Saved from Code", self.by_name["target","country"][-1]["body"])

    def test_missing_snapshot_returns_error(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(lookup.main(["--root", directory, "--kind", "datatype", "Country.GetName"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
