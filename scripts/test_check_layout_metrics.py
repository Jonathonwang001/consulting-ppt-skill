"""Synthetic-only tests; no deck is rendered or accepted by this suite."""
import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from check_layout_metrics import lint, main, REVIEW_KEYS


def rectangle(x=0, y=0, width=100, height=100):
    return dict(x=x, y=y, width=width, height=height)


def sample():
    return {"schema_version": "1.0", "provenance": {
        "kind": "synthetic", "artifact": "unit-test-only", "method": "hand-built bbox"},
        "slides": [{"id": "s1", "canvas": {"width": 1000, "height": 600},
                    "elements": [{"id": "t1", "kind": "text",
                                  "frame": rectangle(50, 50, 200, 100),
                                  "content_box": rectangle(60, 60, 180, 80),
                                  "ink_bounds": rectangle(65, 65, 160, 60)}],
                    "review": dict.fromkeys(REVIEW_KEYS, True)}]}


class LayoutMetricsTests(unittest.TestCase):
    def setUp(self):
        self.data = sample()
        self.slide = self.data["slides"][0]
        self.element = self.slide["elements"][0]

    def run_lint(self, **kwargs):
        return lint(self.data, allow_synthetic=True, **kwargs)

    def assert_error(self, result, code=None):
        self.assertEqual(result["status"], "error")
        self.assertFalse(result["real_slide_acceptance"])
        if code:
            self.assertIn(code, [e["code"] for e in result["errors"]])

    def test_synthetic_default_is_error(self):
        self.assert_error(lint(self.data), "synthetic")

    def test_allow_synthetic_is_never_real_acceptance(self):
        result = self.run_lint()
        self.assertEqual(result["status"], "synthetic_test_ok")
        self.assertFalse(result["real_slide_acceptance"])
        self.assertEqual(result["notice"], "NOT REAL-SLIDE ACCEPTANCE")

    def test_declared_real_contract_never_certifies_actual_deck(self):
        # This remains a fabricated fixture, testing a declared provenance flag only.
        self.data["provenance"]["kind"] = "render_measured"
        result = lint(self.data)
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["declared_metrics_pass"])
        self.assertFalse(result["real_slide_acceptance"])

    def test_ink_inside_frame_but_content_box_insufficient(self):
        self.element["content_box"] = rectangle(60, 60, 100, 80)
        result = self.run_lint()
        self.assert_error(result, "overflow")
        self.assertTrue(any(e["path"].endswith("ink_bounds/content_box")
                            for e in result["errors"]))

    def test_frame_outside_canvas_never_permitted(self):
        self.element["frame"] = rectangle(-0.01, 0, 300, 200)
        self.assert_error(self.run_lint(epsilon=0.5), "overflow")

    def chart(self):
        self.element.update(kind="chart_label", frame=rectangle(50, 50, 250, 200),
                            ink_bounds=rectangle(100, 150, 100, 30),
                            region=rectangle(50, 50, 250, 200))
        del self.element["content_box"]

    def test_chart_label_region_leak(self):
        self.chart()
        self.element["region"] = rectangle(50, 50, 100, 100)
        self.assert_error(self.run_lint(), "overflow")

    def test_legend_outside_plot_inside_safe_region_is_legal(self):
        self.chart()
        plot = rectangle(50, 50, 200, 80)
        self.assertGreater(self.element["ink_bounds"]["y"], plot["y"] + plot["height"])
        self.assertEqual(self.run_lint()["status"], "synthetic_test_ok")

    def test_missing_required_text_metrics(self):
        for key in ("ink_bounds", "content_box", "frame"):
            with self.subTest(key=key):
                data = sample()
                del data["slides"][0]["elements"][0][key]
                self.assert_error(lint(data, allow_synthetic=True), "rect")

    def test_missing_chart_region_and_ink(self):
        self.chart()
        for key in ("region", "ink_bounds"):
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                del data["slides"][0]["elements"][0][key]
                self.assert_error(lint(data, allow_synthetic=True), "rect")

    def test_clipped_text_manual_review_false(self):
        self.slide["review"]["glyph_clipping_checked"] = False
        self.assert_error(self.run_lint(), "review")

    def test_truncated_text_manual_review_false(self):
        self.slide["review"]["complete_text_checked"] = False
        self.assert_error(self.run_lint(), "review")

    def test_all_manual_guards_required_literal_true(self):
        for key in REVIEW_KEYS:
            for value in (False, 1, "true", None):
                with self.subTest(key=key, value=value):
                    self.slide["review"] = dict.fromkeys(REVIEW_KEYS, True)
                    self.slide["review"][key] = value
                    self.assert_error(self.run_lint(), "review")

    def test_missing_review(self):
        del self.slide["review"]
        self.assert_error(self.run_lint(), "review")

    def test_numeric_boolean_rejected(self):
        for key in ("x", "y", "width", "height"):
            with self.subTest(key=key):
                self.element["frame"] = rectangle()
                self.element["frame"][key] = True
                self.assert_error(self.run_lint(), "rect")

    def test_nonfinite_and_huge_numbers_do_not_crash(self):
        for value in (float("nan"), float("inf"), -float("inf"), 10 ** 1000):
            with self.subTest(type=type(value).__name__):
                self.element["frame"] = rectangle(x=value)
                self.assert_error(self.run_lint(), "rect")

    def test_zero_and_negative_dimensions_rejected(self):
        for value in (0, -1):
            for box in ("frame", "content_box", "ink_bounds"):
                with self.subTest(value=value, box=box):
                    data = sample()
                    data["slides"][0]["elements"][0][box]["width"] = value
                    self.assert_error(lint(data, allow_synthetic=True), "rect_size")

    def test_canvas_must_be_positive_finite_nonbool(self):
        for value in (False, 0, -10, float("inf"), float("nan"), "1000"):
            with self.subTest(value=value):
                self.slide["canvas"]["width"] = value
                self.assert_error(self.run_lint())

    def test_invalid_epsilon(self):
        for epsilon in (True, -0.1, 0.5001, float("nan"), float("inf"), "0", None):
            with self.subTest(epsilon=epsilon):
                self.assert_error(self.run_lint(epsilon=epsilon), "epsilon")

    def test_half_pixel_leak_requires_remeasure_not_pass(self):
        self.element["ink_bounds"]["x"] = 59.75
        result = self.run_lint(epsilon=0.5)
        self.assert_error(result, "measurement_uncertainty")
        self.assertIn("NOT design permission", result["errors"][0]["message"])

    def test_zero_epsilon_and_larger_leak_are_overflow(self):
        self.element["ink_bounds"]["x"] = 59.75
        self.assert_error(self.run_lint(), "overflow")
        self.element["ink_bounds"]["x"] = 59
        self.assert_error(self.run_lint(epsilon=0.5), "overflow")

    def test_epsilon_boundaries_without_leak(self):
        for epsilon in (0, 0.5):
            self.assertEqual(self.run_lint(epsilon=epsilon)["status"], "synthetic_test_ok")

    def test_malformed_roots(self):
        for root in (None, [], "bad", 7, True, float("nan"), float("inf"), {}):
            with self.subTest(type=type(root).__name__):
                self.assert_error(lint(root, allow_synthetic=True))

    def test_malformed_collections_and_dicts(self):
        for key, values in (("slides", (None, {}, [], [None], [3])),):
            for value in values:
                data = sample()
                data[key] = value
                self.assert_error(lint(data, allow_synthetic=True))
        for key in ("canvas", "review", "elements"):
            for value in (None, "x", 7, []):
                data = sample()
                data["slides"][0][key] = value
                self.assert_error(lint(data, allow_synthetic=True))
        self.slide["elements"] = [None, 7, [], {}]
        self.assert_error(self.run_lint())

    def test_duplicate_slide_ids(self):
        self.data["slides"].append(copy.deepcopy(self.slide))
        self.assert_error(self.run_lint(), "duplicate_id")

    def test_duplicate_element_ids(self):
        self.slide["elements"].append(copy.deepcopy(self.element))
        self.assert_error(self.run_lint(), "duplicate_id")

    def test_element_ids_are_scoped_per_slide(self):
        slide = copy.deepcopy(self.slide)
        slide["id"] = "s2"
        self.data["slides"].append(slide)
        self.assertEqual(self.run_lint()["status"], "synthetic_test_ok")

    def test_invalid_ids(self):
        for value in (None, "", "  ", True, [], {}):
            self.element["id"] = value
            self.assert_error(self.run_lint(), "id")

    def test_outside_canvas_opt_out_rejected(self):
        for value in (True, 0, "false", None):
            self.element["intentionally_outside_canvas"] = value
            self.assert_error(self.run_lint(), "outside_intent")

    def test_full_canvas_background_legal(self):
        self.slide["elements"].append({"id": "bg", "kind": "shape",
                                      "frame": rectangle(0, 0, 1000, 600)})
        self.assertEqual(self.run_lint()["status"], "synthetic_test_ok")

    def test_images_and_ink_and_region_must_stay_in_canvas(self):
        for kind in ("shape", "image"):
            self.slide["elements"] = [{"id": "s", "kind": kind,
                                       "frame": rectangle(999, 0, 2, 10)}]
            self.assert_error(self.run_lint(), "overflow")
        self.chart()
        self.slide["elements"] = [self.element]
        self.element["region"] = rectangle(-1, 0, 300, 250)
        self.assert_error(self.run_lint(), "overflow")

    def test_bad_schema_kind_and_provenance(self):
        for key in ("schema_version", "provenance"):
            data = sample()
            del data[key]
            self.assert_error(lint(data, allow_synthetic=True))
        for value in (None, [], {}, {"kind": "unknown"}, {"kind": "synthetic"}):
            self.data["provenance"] = value
            self.assert_error(self.run_lint(), "provenance")
        self.data = sample()
        self.data["slides"][0]["elements"][0]["kind"] = []
        self.assert_error(self.run_lint(), "kind")

    def test_derived_edges_nonfinite(self):
        self.element["frame"] = rectangle(1e308, 0, 1e308, 100)
        self.assert_error(self.run_lint(), "rect")

    def test_invalid_synthetic_flag_type(self):
        self.assert_error(lint(self.data, allow_synthetic="yes"), "allow_synthetic")

    def test_input_unchanged(self):
        before = copy.deepcopy(self.data)
        self.run_lint()
        self.assertEqual(self.data, before)

    def test_cli_synthetic_banner_and_default_failure(self):
        for flag, expected in (([], 1), (["--allow-synthetic"], 0)):
            with patch("builtins.open", return_value=io.StringIO(json.dumps(sample()))):
                with redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(main(["unit.json"] + flag), expected)
            result = json.loads(output.getvalue())
            self.assertFalse(result["real_slide_acceptance"])
            self.assertEqual(result["notice"], "NOT REAL-SLIDE ACCEPTANCE")

    def test_cli_bad_json_and_missing_file(self):
        for failure in (False, True):
            with patch("builtins.open") as opener:
                if failure:
                    opener.side_effect = FileNotFoundError("missing")
                else:
                    opener.return_value = io.StringIO("{bad json")
                with redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(main(["bad.json"]), 1)
            self.assert_error(json.loads(output.getvalue()), "input")


if __name__ == "__main__":
    unittest.main()
