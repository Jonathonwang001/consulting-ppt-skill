#!/usr/bin/env python3
"""Lint planning JSON, not rendered slides or factual correctness. Standard library only."""
import argparse
import json
import re
import sys
from pathlib import Path

RELATIONS = {"parallel", "sequence", "causal", "hierarchy", "comparison", "conversion", "time", "ecosystem", "tradeoff", "quantitative", "navigation"}
STATUSES = {"verified", "client_provided", "hypothesis", "illustrative"}
STRUCTURAL = {"cover", "agenda", "divider", "appendix_index"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def lint(doc):
    errors, warnings = [], []
    if not isinstance(doc, dict):
        return ["root: expected object"], []
    for key in ("schema_version", "project"):
        if not nonempty(doc.get(key)):
            errors.append(f"root: missing {key}")
    slides = doc.get("slides")
    if not isinstance(slides, list) or not slides:
        return errors + ["root: slides must be a nonempty list"], warnings
    ids = set()
    for index, slide in enumerate(slides, 1):
        at = f"slide[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{at}: expected object")
            continue
        for key in ("id", "type", "title", "reader_decision", "visual_unit", "metric_unit"):
            if not nonempty(slide.get(key)):
                errors.append(f"{at}: missing {key}")
        sid = slide.get("id")
        if nonempty(sid):
            if sid in ids:
                errors.append(f"{at}: duplicate id {sid}")
            ids.add(sid)
        relation = slide.get("relation")
        status = slide.get("evidence_status")
        slide_type = slide.get("type")
        if not isinstance(relation, str) or relation not in RELATIONS:
            errors.append(f"{at}: invalid or missing relation")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{at}: invalid or missing evidence_status")
        sources = slide.get("sources", [])
        if not isinstance(sources, list) or any(not nonempty(x) for x in sources):
            errors.append(f"{at}: sources must be a list of nonempty strings")
        elif (not isinstance(slide_type, str) or slide_type not in STRUCTURAL) and not sources:
            errors.append(f"{at}: missing source or explicit hypothesis/illustrative provenance")
        icons = slide.get("icons", [])
        if not isinstance(icons, list):
            errors.append(f"{at}: icons must be a list")
            icons = []
        if not icons and not nonempty(slide.get("no_icon_reason")):
            errors.append(f"{at}: provide no_icon_reason when icons are omitted")
        families = set()
        for j, icon in enumerate(icons, 1):
            if not isinstance(icon, dict):
                errors.append(f"{at}.icon[{j}]: expected object")
                continue
            for key in ("concept", "semantic_role", "family", "placement", "asset_source"):
                if not nonempty(icon.get(key)):
                    errors.append(f"{at}.icon[{j}]: missing {key}")
            if nonempty(icon.get("family")):
                families.add(icon["family"])
            if icon.get("semantic_role") == "quantitative" and not nonempty(icon.get("metric_mapping")):
                errors.append(f"{at}.icon[{j}]: quantitative icon needs metric_mapping")
        if len(families) > 1:
            warnings.append(f"{at}: mixed icon families; review optical consistency")
        if len(icons) > 6:
            warnings.append(f"{at}: many icons; review density and whether they aid identification")
        geometry = slide.get("geometry")
        if not isinstance(geometry, dict):
            errors.append(f"{at}: missing geometry declaration")
        else:
            for key in ("quantitative", "proportional"):
                if not isinstance(geometry.get(key), bool):
                    errors.append(f"{at}.geometry: {key} must be boolean")
            if geometry.get("proportional") and not geometry.get("quantitative"):
                errors.append(f"{at}.geometry: proportional requires quantitative=true")
            if not nonempty(geometry.get("basis")):
                errors.append(f"{at}.geometry: missing basis or explicit not-to-scale statement")
        if isinstance(relation, str) and relation in {"causal", "sequence", "ecosystem"} and not nonempty(slide.get("connector_meaning")):
            errors.append(f"{at}: connector_meaning required for connected relationships")
        title = slide.get("title") if isinstance(slide.get("title"), str) else ""
        if slide.get("evidence_status") == "hypothesis" and not re.search(r"假设|待验证|拟|可能|hypothes|propos|may|test", title, re.I):
            warnings.append(f"{at}: title may overstate an unverified hypothesis")
    mapping = doc.get("question_workstream_map", [])
    if not isinstance(mapping, list):
        errors.append("root: question_workstream_map must be a list")
    else:
        if any(isinstance(s, dict) and s.get("type") == "work_plan" for s in slides) and not mapping:
            errors.append("root: work_plan requires question_workstream_map")
        question_ids = set()
        for i, row in enumerate(mapping, 1):
            at = f"map[{i}]"
            if not isinstance(row, dict):
                errors.append(f"{at}: expected object")
                continue
            for key in ("question_id", "question", "hypothesis", "method", "workstream", "owner", "deliverable", "client_input", "checkpoint"):
                if not nonempty(row.get(key)):
                    errors.append(f"{at}: missing {key}")
            qid = row.get("question_id")
            if nonempty(qid):
                if qid in question_ids:
                    warnings.append(f"{at}: repeated question_id; check one-to-many mapping is intentional")
                question_ids.add(qid)
    brand = doc.get("brand", {})
    if not isinstance(brand, dict):
        errors.append("root: brand must be object")
    elif "deloitte" in str(brand.get("preset", "")).lower() and str(brand.get("primary", "")).upper() == "#86BC25":
        errors.append("brand: Deloitte-inspired uses black/charcoal/blue-grey primary, not green primary")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        doc = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors, warnings = lint(doc)
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")
    print("Scope: planning structure only; manual semantic, source, asset and rendering review still required.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
