#!/usr/bin/env python3
"""Regression cases for planning lint rules, with no third-party dependencies."""
import copy
import json
import unittest
from pathlib import Path
from lint_slide_brief import lint

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / "templates" / "slide-brief.example.json").read_text())


class BriefTests(unittest.TestCase):
    def test_example(self):
        self.assertEqual(lint(EXAMPLE), ([], []))

    def test_root(self):
        self.assertTrue(lint([])[0])

    def test_no_icons_valid(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["icons"] = []
        doc["slides"][0]["no_icon_reason"] = "Data table needs labels, not decoration"
        self.assertFalse(lint(doc)[0])

    def test_missing_icon_reason(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][1]["no_icon_reason"] = ""
        self.assertTrue(any("no_icon_reason" in x for x in lint(doc)[0]))

    def test_mixed_families_warn(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["icons"][1]["family"] = "outline"
        self.assertTrue(lint(doc)[1])

    def test_quantitative_icon_mapping(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["icons"][0]["semantic_role"] = "quantitative"
        self.assertTrue(any("metric_mapping" in x for x in lint(doc)[0]))

    def test_geometry(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["geometry"]["proportional"] = True
        self.assertTrue(any("proportional requires" in x for x in lint(doc)[0]))

    def test_missing_source(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["sources"] = []
        self.assertTrue(any("missing source" in x for x in lint(doc)[0]))

    def test_workstream_closed_loop(self):
        doc = copy.deepcopy(EXAMPLE)
        del doc["question_workstream_map"][0]["deliverable"]
        self.assertTrue(any("deliverable" in x for x in lint(doc)[0]))

    def test_duplicate_slide(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][1]["id"] = "S1"
        self.assertTrue(any("duplicate id" in x for x in lint(doc)[0]))

    def test_deloitte_green(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["brand"]["primary"] = "#86BC25"
        self.assertTrue(any("Deloitte" in x for x in lint(doc)[0]))

    def test_connector_semantics(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["relation"] = "causal"
        self.assertTrue(any("connector_meaning" in x for x in lint(doc)[0]))

    def test_malformed_values(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["slides"][0]["title"] = ["invalid"]
        doc["slides"][0]["icons"] = [None]
        doc["slides"][0]["sources"] = 5
        doc["question_workstream_map"] = [None]
        self.assertGreaterEqual(len(lint(doc)[0]), 3)
        for bad in ([], {}):
            for key in ("relation", "evidence_status", "type"):
                case = copy.deepcopy(EXAMPLE)
                case["slides"][0][key] = bad
                self.assertTrue(lint(case)[0], key)


if __name__ == "__main__":
    unittest.main()
