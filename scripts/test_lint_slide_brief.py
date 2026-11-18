#!/usr/bin/env python3
"""Regression cases for planning lint rules, with no third-party dependencies."""
import copy
import json
import unittest
from pathlib import Path
from lint_slide_brief import lint

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / "templates" / "slide-brief.example.json").read_text())
INTERNAL = json.loads((Path(__file__).resolve().parents[1] / "templates" / "internal-report.example.json").read_text())


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

    def test_internal_no_client_map(self):
        self.assertNotIn("question_workstream_map", INTERNAL)
        self.assertEqual(lint(INTERNAL), ([], []))

    def test_external_report_no_proposal_map(self):
        doc = copy.deepcopy(INTERNAL)
        doc["scenario"] = "external_report"
        for page in doc["slides"]:
            page["scenario"] = "external_report"
        self.assertEqual(lint(doc), ([], []))

    def test_external_report_plan_needs_tracking_not_client_map(self):
        doc = copy.deepcopy(INTERNAL)
        doc["scenario"] = "external_report"
        for page in doc["slides"]:
            page["scenario"] = "external_report"
        del doc["slides"][1]["action_tracking"]
        self.assertTrue(any("action_tracking" in e for e in lint(doc)[0]))
        self.assertFalse(any("requires question_workstream_map" in e for e in lint(doc)[0]))

    def test_legacy_20_compatible(self):
        doc = copy.deepcopy(EXAMPLE)
        doc["schema_version"] = "2.0"
        for key in ("scenario", "audience", "reader_task", "reading_mode", "layout_contract"):
            del doc[key]
        for slide in doc["slides"]:
            del slide["evidence_modules"]
        self.assertEqual(lint(doc), ([], []))

    def test_scene_fields_required(self):
        for key in ("scenario", "audience", "reader_task", "reading_mode", "layout_contract"):
            doc = copy.deepcopy(INTERNAL)
            del doc[key]
            self.assertTrue(lint(doc)[0], key)

    def test_external_plan_still_needs_map(self):
        doc = copy.deepcopy(EXAMPLE)
        del doc["question_workstream_map"]
        self.assertTrue(any("requires question_workstream_map" in x for x in lint(doc)[0]))

    def test_internal_tracking_required(self):
        doc = copy.deepcopy(INTERNAL)
        del doc["slides"][1]["action_tracking"]
        self.assertTrue(any("action_tracking" in x for x in lint(doc)[0]))

    def test_composite_module_support(self):
        doc = copy.deepcopy(INTERNAL)
        del doc["slides"][0]["evidence_modules"][1]["supports"]
        self.assertTrue(any("supports" in x for x in lint(doc)[0]))

    def test_zero_overflow_policy_required(self):
        doc = copy.deepcopy(INTERNAL)
        doc["layout_contract"]["overflow_policy"] = "auto_shrink_or_clip"
        self.assertTrue(any("zero_overflow" in x for x in lint(doc)[0]))

    def test_mixed_requires_concrete_slide_scene(self):
        doc = copy.deepcopy(INTERNAL)
        doc["scenario"] = "mixed"
        self.assertTrue(lint(doc)[0])
        for slide in doc["slides"]:
            slide["scenario"] = "internal_working"
        self.assertFalse(lint(doc)[0])

    def test_invalid_or_mismatched_scene_cannot_bypass_external_map(self):
        for bad in ("typo", [], {}, None, "internal_executive", "external_report", "mixed"):
            with self.subTest(scene=bad):
                doc = copy.deepcopy(EXAMPLE)
                del doc["question_workstream_map"]
                for slide in doc["slides"]:
                    slide["scenario"] = bad
                self.assertTrue(any("scenario" in item for item in lint(doc)[0]))

if __name__ == "__main__":
    unittest.main()
