# BD Strategy & Data Visualization Review Rubric

Use this rubric when auditing the **Shopee at the Crossroads** project (or similar BD strategy case studies) to surface non-obvious weaknesses that elevate the work from a "good student project" to an "executive-ready McKinsey / Sea Group BD portfolio piece."

---

## Pillar 1: Data & Analytical Rigor

1. **Public Data vs. Derived Assumptions Transparency:**
   - **Weakness to look for:** Mixing hard public filings (e.g., DBD revenue/profit, Cube Asia annual GMV) with analyst-scored matrices (e.g., 1–10 threat scores, 1–5 regulatory impact scores, 18-month ROI scenarios) without explicitly documenting the **scoring rubric / weighting formula** inside the notebooks.
   - **How to improve:** Add explicit scoring methodology tables or sensitivity formulas in notebooks (`02_threat_landscape.ipynb`, `04_regulatory_wind.ipynb`, `05_strategic_options.ipynb`) so a skeptical reader knows *why* TikTok Shop scored 8.4/10 on counter-difficulty or how the `+24.5%` Base Case ROI was calculated.

2. **Consolidated Entity Scope (Marketplace vs. Logistics):**
   - **Weakness to look for:** Analyzing `บจก. ช้อปปี้ (ประเทศไทย)` (Marketplace) in isolation from `บจก. เอสพีเอ็กซ์ เอ็กซ์เพรส (ประเทศไทย)` (SPX Express) in Section 3, even though SPX Express is a core pillar of the recommendation in Section 6.
   - **How to improve:** Show both standalone Marketplace financials and the **Consolidated Sea Thailand E-Commerce + Logistics ecosystem view** (where SPX Express adds 23,499M THB revenue and +469M THB profit).

3. **Unit Economics & Financial Bridge:**
   - **Weakness to look for:** Recommending a margin recovery from `3.1% -> >5.5%` in `memo.md` without showing a quantitative **P&L / Margin Bridge** (how much margin comes from cutting blanket live-stream subsidies vs. Ads take-rate expansion vs. SPX fulfillment scale).

---

## Pillar 2: Chart & Visual Storytelling Quality

1. **Title & Subtitle Discipline (Section 9 Rules):**
   - Every chart title must state the **core takeaway** (e.g., *"TikTok Shop แซง Shopee ครั้งแรกใน Q2 2026..."*), while the subtitle states the **metric, unit, and time horizon**.
2. **Annotation & Visual Hierarchy:**
   - **Weakness to look for:** Callout boxes that overlap data points, bars, legends, or axis lines; small font sizes on high-DPI exports; or missing direct data labels on bars/lines.
   - **How to improve:** Ensure generous whitespace around annotations, add direct threshold lines (e.g., industry benchmark or target margin guardrails), and keep legend markers proportional.
3. **Color & Typography Consistency:**
   - Shopee = `#EE4D2D` (Orange), TikTok Shop = `#111111` (Black) / `#FE2C55` (Red for loss/alert), Lazada = `#0F146D` (Blue), Temu = `#2E8B57` (Green), OTOP/Tailwind = `#198754` (Emerald).
   - Zero missing glyphs (`[A]` or tofu boxes) across Thai and English text.

---

## Pillar 3: Strategic & BD Logic (The "Skeptical VP" Test)

Ask these hard questions when reviewing the notebooks and `memo.md`:

1. **Competitor Counter-Move Blind Spot:**
   - *What if TikTok Shop aggressively expands TikTok Shop Mall and partners with J&T/Flash for Next-Day Delivery, or launches its own OTOP subsidy program?*
   - A strong BD analysis includes a **"Competitive Counter-Response & Mitigation"** table explaining why Shopee's moat still holds (e.g., SPX Express first-party hub density + multi-SKU search basket economics).
2. **Seller Retention Mechanics:**
   - Section 3 shows small sellers only keep `~8%` net margin after `34.7%` platform costs. How does Shopee prevent small sellers from churning to TikTok Shop without cutting Shopee's own take-rate further?
   - The recommendation should specify **tiered fee relief tied to Ads/SPX adoption** or **AI-assisted seller tools** that improve conversion rate (lowering effective ad cost per order).
3. **Resource Allocation Math (50 : 30 : 20):**
   - Translate the `50 : 30 : 20` split into concrete budget/headcount terms (e.g., out of the ~3,850M THB strategic investment envelope across Options 1, 2, and 3: ~1,200M THB to Core Intent/SPX, ~850M THB to OTOP/Local SME, and ~1,800M THB capped for Surgical Affiliate).

---

## Pillar 4: Executive Communication (`memo.md` & `README.md`)

1. **Thai-English Balance for Thai Tech/BD Readers:**
   - Narrative context should read naturally in fluent executive Thai, while retaining industry-standard English BD terms (*GMV Share*, *Unit Economics*, *Take-rate*, *Structural Moat*, *Impulse vs. Intent*, *SLA*, *ROI*, *EBITDA*).
2. **Notebook Narrative Depth:**
   - Check whether the markdown cells inside `notebooks/01` through `06` are too brief compared to `README.md`. Notebooks should contain rich executive commentary, methodology notes for scored matrices, and summary tables so anyone opening a `.ipynb` file gets the full analysis.
