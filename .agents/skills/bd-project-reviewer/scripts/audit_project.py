#!/usr/bin/env python3
"""Automated Technical & Content Depth Audit for Shopee BD Analysis Project."""

import os
import re
import sys
import json
import pandas as pd
from PIL import Image


def audit_project(project_dir: str):
    print("=" * 72)
    print(f"BD PROJECT AUTOMATED AUDIT: {project_dir}")
    print("=" * 72)

    findings = []

    # 1. Check Required Directories & Core Files
    required_paths = [
        "data/raw/data_sources_and_notes.md",
        "data/raw/raw_market_gmv.csv",
        "data/raw/raw_dbd_financials.csv",
        "data/raw/raw_fees_and_regulations.csv",
        "memo.md",
        "README.md",
    ]
    print("\n[1] Core Structure & Files Check:")
    for rel in required_paths:
        full = os.path.join(project_dir, rel)
        exists = os.path.exists(full)
        size = os.path.getsize(full) if exists else 0
        status = "OK" if exists and size > 0 else "MISSING/EMPTY"
        print(f"  - {rel:<42} [{status}] ({size:,} bytes)")
        if status != "OK":
            findings.append(f"[HIGH] Core file missing or empty: {rel}")

    # 2. Check Processed CSV Tables
    proc_dir = os.path.join(project_dir, "data/processed")
    print("\n[2] Processed Datasets Check (data/processed/):")
    if os.path.isdir(proc_dir):
        csv_files = sorted(f for f in os.listdir(proc_dir) if f.endswith(".csv"))
        for f in csv_files:
            df = pd.read_csv(os.path.join(proc_dir, f))
            nulls = int(df.isna().sum().sum())
            print(f"  - {f:<38} rows={len(df):<3} cols={len(df.columns):<2} nulls={nulls}")
            if nulls > 0:
                findings.append(f"[MED] Dataset {f} contains {nulls} null values.")
    else:
        findings.append("[HIGH] data/processed/ directory is missing.")

    # 3. Check Notebooks (Execution State & Narrative Depth)
    nb_dir = os.path.join(project_dir, "notebooks")
    print("\n[3] Jupyter Notebooks Check (Execution & Markdown Depth):")
    if os.path.isdir(nb_dir):
        nbs = sorted(f for f in os.listdir(nb_dir) if f.endswith(".ipynb"))
        for nb_file in nbs:
            nb_path = os.path.join(nb_dir, nb_file)
            with open(nb_path, "r", encoding="utf-8") as fh:
                nb_data = json.load(fh)
            cells = nb_data.get("cells", [])
            md_cells = [c for c in cells if c.get("cell_type") == "markdown"]
            code_cells = [c for c in cells if c.get("cell_type") == "code"]
            unexecuted = [i for i, c in enumerate(code_cells) if not c.get("outputs")]
            md_char_count = sum(len("".join(c.get("source", []))) for c in md_cells)

            print(
                f"  - {nb_file:<32} md_cells={len(md_cells)} "
                f"code_cells={len(code_cells)} unexecuted={len(unexecuted)} "
                f"md_chars={md_char_count:,}"
            )
            if unexecuted:
                findings.append(f"[HIGH] {nb_file} has {len(unexecuted)} unexecuted code cell(s).")
            if md_char_count < 800:
                findings.append(
                    f"[MED] Narrative depth in {nb_file} is relatively brief ({md_char_count} chars); "
                    "consider adding scoring methodology / deeper BD commentary."
                )

    # 4. Check Charts (Resolution & DPI)
    charts_dir = os.path.join(project_dir, "charts")
    print("\n[4] Matplotlib Charts Check (charts/*.png):")
    if os.path.isdir(charts_dir):
        pngs = sorted(f for f in os.listdir(charts_dir) if f.endswith(".png"))
        print(f"  Total PNG charts found: {len(pngs)}")
        for png in pngs:
            p = os.path.join(charts_dir, png)
            with Image.open(p) as img:
                w, h = img.size
                dpi = img.info.get("dpi", (0, 0))
                dpi_x = round(dpi[0]) if dpi else 0
                print(f"  - {png:<40} {w}x{h}px  DPI={dpi_x}")
                if dpi_x < 299:
                    findings.append(f"[MED] Chart {png} DPI is {dpi_x} (expected 300 DPI).")

    # 5. Check Markdown Links in README.md & memo.md
    print("\n[5] Markdown Local Link & Image Reference Check:")
    link_pattern = re.compile(r"!?\[.*?\]\((\./[^)]+)\)")
    for md_name in ["README.md", "memo.md"]:
        md_path = os.path.join(project_dir, md_name)
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            links = link_pattern.findall(content)
            broken = [lnk for lnk in links if not os.path.exists(os.path.join(project_dir, lnk))]
            print(f"  - {md_name:<15} local_links={len(links)} broken={len(broken)}")
            for b in broken:
                findings.append(f"[HIGH] Broken relative link in {md_name}: {b}")

    print("\n" + "=" * 72)
    print(f"AUTOMATED DIAGNOSTIC SUMMARY ({len(findings)} Automated Flags):")
    if not findings:
        print("  All automated structural & technical checks passed!")
    else:
        for idx, item in enumerate(findings, 1):
            print(f"  {idx}. {item}")
    print("=" * 72)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/home/windows/Projects/Lab/shopee-bd-analysis"
    audit_project(target)
