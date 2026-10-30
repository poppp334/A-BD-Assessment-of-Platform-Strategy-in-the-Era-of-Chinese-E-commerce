---
name: bd-project-reviewer
description: >-
  Use this skill when the user asks to review, critique, audit, or find weaknesses
  and areas for improvement in the Shopee BD Assessment project (or any data-driven
  BD strategy project). It diagnoses analytical, visual, strategic, and narrative
  weaknesses and presents a prioritized improvement report, strictly waiting for
  human approval before modifying any files.
---

# BD Project Reviewer & Improvement Gatekeeper (`bd-project-reviewer`)

This skill provides a structured, executive-grade review workflow to identify weaknesses, blind spots, and improvement opportunities across data pipelines, Jupyter notebooks, Matplotlib visualizations, and executive BD deliverables (`memo.md` and `README.md`).

> **STRICT HUMAN-IN-THE-LOOP RULE:**
> When executing a review, you operate in **Read-Only Diagnostic Mode** until the user approves changes. You **MUST NOT** edit any project files (`data/`, `notebooks/`, `charts/`, `memo.md`, `README.md`) before presenting the Weakness & Improvement Report and receiving explicit human approval.

---

## Workflow Steps

### Step 1: Run the Automated Technical Audit
Run the diagnostic script [audit_project.py](./scripts/audit_project.py) to check structural completeness, dataset cross-consistency, notebook execution state, chart image dimensions/DPI, and markdown link integrity:

```bash
/home/windows/Projects/Lab/shopee-bd-analysis/.venv/bin/python /home/windows/Projects/Lab/.agents/skills/bd-project-reviewer/scripts/audit_project.py /home/windows/Projects/Lab/shopee-bd-analysis
```

### Step 2: Conduct Deep BD & Visual Critique
Read the evaluation criteria in [review_rubric.md](./references/review_rubric.md) and compare the current project artifacts against the blueprint (`/home/windows/Projects/Lab/project_doc_shopee.md`):

1. **Data & Analytical Rigor (`data/raw/` & `data/processed/`):**
   - Check for unstated assumptions, unit mismatches (USD bn vs. THB mn, BE vs. CE years), or missing sensitivity bounds.
   - Verify whether financial bridge math (GMV -> Take-rate -> Revenue -> Net Profit) is explicitly quantified.
2. **Chart & Visual Storytelling Quality (`charts/*.png`):**
   - Use `read_file` to visually inspect the PNG charts in `charts/`.
   - Check for label overlaps, crowded callout boxes, weak titles that describe axes instead of insights, missing data labels, or inconsistent brand colors.
3. **Strategic & BD Logic (`notebooks/` & `memo.md`):**
   - Challenge the strategic thesis like a skeptical Sea Group / Shopee Regional VP:
     - Are competitor counter-moves (e.g., TikTok Shop launching Mall/Next-Day delivery or matching OTOP incentives) addressed?
     - Are the 50:30:20 resource allocation numbers backed by an explicit financial bridge showing how net margin recovers from `3.1%` to `>5.5%`?
     - Are seller churn risks and unit economics quantified?
4. **Executive Communication (`memo.md` & `README.md`):**
   - Evaluate readability for Thai readers while preserving sharp English BD terminology.
   - Check if any section is repetitive, overly verbose, or missing concrete North-Star KPIs.

### Step 3: Present the Weakness & Improvement Report (Wait for Approval)
Output a clear, structured report in the chat organized as follows:

1. **Automated Audit Health Check:** Summary of technical checks from `audit_project.py`.
2. **Identified Weaknesses & Improvement Opportunities (Prioritized Table):**
   | ID | Category (Data / Chart / Strategy / Narrative) | Severity / Impact | Target File(s) | Weakness Identified | Proposed Improvement |
   |---|---|---|---|---|---|
   | **W1** | ... | High / Med / Low | ... | ... | ... |
3. **Approval Prompt:** Ask the user which item IDs (e.g., *"Approve all"*, or *"Do W1, W2, and W4"*) they want you to implement. **End your turn here and wait for the user's decision.**

### Step 4: Execute Approved Improvements & Verify
Once (and only once) the user approves specific items:
1. Implement the approved changes across `data/`, `notebooks/`, `memo.md`, and/or `README.md`.
2. Re-execute affected notebooks so inline outputs and `charts/*.png` (300 DPI) are regenerated.
3. Visually inspect every modified chart using `read_file` to confirm zero text overlap and clean Thai + English rendering.
4. Re-run [audit_project.py](./scripts/audit_project.py) to verify all checks pass.
