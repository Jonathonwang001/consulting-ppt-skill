#!/usr/bin/env python3
"""Lint declared pixel metrics, not PPTX, glyph generation, or source truth."""
import argparse
import json
import math
import sys

REVIEW_KEYS = ("complete_text_checked", "glyph_clipping_checked",
               "font_substitution_checked", "occlusion_checked")
KINDS = ("text", "chart_label", "shape", "image")


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, ValueError):
        return False


def lint(data, epsilon=0.0, allow_synthetic=False):
    """Return JSON-safe findings. Synthetic test success is never acceptance."""
    errors = []

    def error(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    valid_epsilon = _number(epsilon) and 0 <= epsilon <= 0.5
    if not valid_epsilon:
        error("epsilon", "$", "epsilon must be finite, non-bool, in [0, 0.5] px")
        epsilon = 0.0
    if not isinstance(allow_synthetic, bool):
        error("allow_synthetic", "$", "allow_synthetic must be a bool")
        allow_synthetic = False
    synthetic = False

    def finish():
        accepted = not errors and not synthetic
        status = "error" if errors else ("synthetic_test_ok" if synthetic else "pass")
        notice = ("NOT REAL-SLIDE ACCEPTANCE" if synthetic else
                  "DECLARED METRICS/REVIEW ONLY; SOURCE TRUTH NOT VERIFIED")
        return {"status": status, "declared_metrics_pass": accepted,
                "real_slide_acceptance": False,
                "notice": notice, "epsilon_px": epsilon, "errors": errors}

    def rect(value, path):
        if not isinstance(value, dict):
            error("rect", path, "required rectangle object is missing or invalid")
            return None
        names = ("x", "y", "width", "height")
        if not all(_number(value.get(k)) for k in names):
            error("rect", path, "x/y/width/height must be finite non-bool numbers")
            return None
        x, y, width, height = (float(value[k]) for k in names)
        if width <= 0 or height <= 0:
            error("rect_size", path, "rectangle width and height must be positive")
            return None
        right, bottom = x + width, y + height
        if not math.isfinite(right) or not math.isfinite(bottom):
            error("rect", path, "derived rectangle edges must be finite")
            return None
        return x, y, right, bottom

    def contained(inner, outer, path, tolerance=0.0):
        if inner is None or outer is None:
            return
        leak = max(outer[0] - inner[0], outer[1] - inner[1],
                   inner[2] - outer[2], inner[3] - outer[3], 0.0)
        if leak > 0:
            uncertain = tolerance > 0 and leak <= tolerance
            error("measurement_uncertainty" if uncertain else "overflow", path,
                  "measured leak %.6g px; %s" % (leak,
                  "remeasure; epsilon is NOT design permission" if uncertain
                  else "zero engineering overflow required"))

    def identifier(value, path, seen):
        if not isinstance(value, str) or not value.strip():
            error("id", path, "id must be a nonempty string")
        elif value in seen:
            error("duplicate_id", path, "id must be unique in its scope")
        else:
            seen.add(value)

    if not isinstance(data, dict):
        error("root", "$", "root must be an object")
        return finish()
    if data.get("schema_version") != "1.0":
        error("schema_version", "$.schema_version", "expected string '1.0'")
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        error("provenance", "$.provenance", "provenance object required")
    else:
        kind = provenance.get("kind")
        synthetic = kind == "synthetic"
        if kind not in ("render_measured", "synthetic"):
            error("provenance", "$.provenance.kind", "unsupported provenance kind")
        if synthetic and not allow_synthetic:
            error("synthetic", "$.provenance.kind", "synthetic input rejected by default")
        for key in ("artifact", "method"):
            value = provenance.get(key)
            if not isinstance(value, str) or not value.strip():
                error("provenance", "$.provenance." + key, "nonempty string required")
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        error("slides", "$.slides", "nonempty slides array required")
        return finish()
    slide_ids = set()
    for si, slide in enumerate(slides):
        sp = "$.slides[%d]" % si
        if not isinstance(slide, dict):
            error("slide", sp, "slide must be an object")
            continue
        identifier(slide.get("id"), sp + ".id", slide_ids)
        canvas = slide.get("canvas")
        if not isinstance(canvas, dict):
            error("canvas", sp + ".canvas", "canvas object required")
            bounds = None
        else:
            bounds = rect(dict(x=0, y=0, width=canvas.get("width"),
                               height=canvas.get("height")), sp + ".canvas")
        review = slide.get("review")
        if not isinstance(review, dict):
            error("review", sp + ".review", "manual review object required")
        else:
            for key in REVIEW_KEYS:
                if review.get(key) is not True:
                    error("review", sp + ".review." + key,
                          "must be literal true after complete manual review")
        elements = slide.get("elements")
        if not isinstance(elements, list) or not elements:
            error("elements", sp + ".elements", "nonempty elements array required")
            continue
        element_ids = set()
        for ei, element in enumerate(elements):
            ep = sp + ".elements[%d]" % ei
            if not isinstance(element, dict):
                error("element", ep, "element must be an object")
                continue
            identifier(element.get("id"), ep + ".id", element_ids)
            kind = element.get("kind")
            if kind not in KINDS:
                error("kind", ep + ".kind", "unsupported element kind")
            if element.get("intentionally_outside_canvas", False) is not False:
                error("outside_intent", ep, "semantic objects cannot opt out of canvas")
            frame = rect(element.get("frame"), ep + ".frame")
            contained(frame, bounds, ep + ".frame/canvas")
            boxes = {}
            required = {"ink_bounds", "content_box"} if kind == "text" else set()
            if kind == "chart_label":
                required = {"ink_bounds", "region"}
            for name in ("ink_bounds", "content_box", "region"):
                if name in element or name in required:
                    boxes[name] = rect(element.get(name), ep + "." + name)
                    contained(boxes[name], bounds, ep + "." + name + "/canvas")
            content = boxes.get("content_box")
            ink = boxes.get("ink_bounds")
            if content is not None:
                contained(content, frame, ep + ".content_box/frame")
                contained(ink, content, ep + ".ink_bounds/content_box", epsilon)
            if kind == "chart_label":
                contained(ink, boxes.get("region"), ep + ".ink_bounds/region", epsilon)
            contained(ink, frame, ep + ".ink_bounds/frame", epsilon)
    return finish()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics", help="UTF-8 JSON of measured actual pixel coordinates")
    parser.add_argument("--epsilon", type=float, default=0.0,
                        help="measurement uncertainty threshold, 0..0.5 px (never permission)")
    parser.add_argument("--allow-synthetic", action="store_true", help="tests only")
    args = parser.parse_args(argv)
    try:
        with open(args.metrics, encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, ValueError, RecursionError) as exc:
        result = {"status": "error", "real_slide_acceptance": False,
                  "declared_metrics_pass": False,
                  "notice": "INPUT NOT VALIDATED", "errors": [
                      {"code": "input", "path": "$", "message": str(exc)}]}
    else:
        result = lint(data, epsilon=args.epsilon, allow_synthetic=args.allow_synthetic)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["status"] in ("pass", "synthetic_test_ok") else 1


if __name__ == "__main__":
    sys.exit(main())
