# NIRF 2025 Engineering College Value-for-Money (VFM) Analytics

> **AccioJob · Spin Build Pitch · Data Analytics · Project DA-16**  
> *"Is that college worth the fees?"*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![NIRF](https://img.shields.io/badge/NIRF-2025%20Engineering%20Rankings-orange.svg)](https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html)
[![Dashboard](https://img.shields.io/badge/Interactive%20Dashboard-Live%20HTML-success.svg)](dashboard.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

---

## Executive Summary & Stakeholder Decision

* **The Stakeholder:** A prospective Indian engineering student and their family deciding among college admission offers.
* **The Decision:** Determining which engineering institution delivers the highest financial return relative to mandatory four-year academic fees, balancing brand prestige against family capital outlays and educational loan burdens.
* **The Problem:** Families routinely compare colleges solely on NIRF ranking and brand reputation. However, tuition fees and placement outcomes diverge wildly: two colleges separated by only a few rank spots can demand an 80× fee difference while offering identical salaries.
* **The Core Value Metric:**
  $$\text{Fee-to-Salary Ratio} = \frac{\text{Total 4-Year Mandatory Academic Fees (General Category)}}{\text{Annual Median Placement Salary}}$$
  *(Represents the equivalent years of gross first-year median salary required to pay back total 4-year tuition and academic dues. Lower is better.)*

---

## Key Analytical Findings

### 1. Public Institutions Deliver Up to 224× Faster Capital Recovery
Highly subsidized state and central government universities dominate the top 10 best-value institutions in India:
* **Jadavpur University** (NIRF #18) charges just **₹14,110** total academic fees over four years against a median salary of **₹10.50 LPA**, recovering academic costs in **0.013 years** (~5 days of gross salary) with a **91.01%** placement rate.
* **Jamia Millia Islamia** (NIRF #24) costs **₹0.66L** for a **₹13.78 LPA** median salary (**0.048 years** / 18 days; 84.6% placed).
* **Anna University CEG** (NIRF #20) costs **₹1.33L** for an **₹8.00 LPA** median salary (**0.166 years** / 2.0 months; 72.4% placed).

Conversely, high-tuition private and deemed universities occupy 9 of the top 10 highest fee-to-salary ratios:
* **SRM IST** (NIRF #14) charges **₹18.10L** in fees for a **₹6.20 LPA** median salary (**2.919 years** / 35.0 months), taking **224× longer** to recover fees than Jadavpur despite holding a higher NIRF rank.
* **UPES Dehradun** (NIRF #43): ₹16.80L fees, ₹6.50 LPA salary $\rightarrow$ **2.585 years** (31.0 months).
* **Vignan's Foundation** (NIRF #80): ₹9.70L fees, ₹3.36 LPA salary $\rightarrow$ **2.887 years** (34.6 months; 43.4% placed).

### 2. The "Mid-Tier Trap" (Rank Bands 2 & 3)
Comparing rank bands reveals that moving from Band 1 (Ranks 1–25) to Bands 2 & 3 (Ranks 26–75) **increases average fees while slashing salaries by 29%**:
* **Band 1 (Ranks 1–25):** Avg Fees **₹8.63L** | Avg Salary **₹15.05 LPA** | Recovery **0.684 yrs** (8.2 mo) | Placed **79.72%**
* **Band 2 (Ranks 26–50):** Avg Fees **₹9.22L** (+6.8%) | Avg Salary **₹10.76 LPA** (-28.5%) | Recovery **0.992 yrs** (11.9 mo) | Placed **71.39%**
* **Band 3 (Ranks 51–75):** Avg Fees **₹9.10L** | Avg Salary **₹10.40 LPA** (-30.9%) | Recovery **0.968 yrs** (11.6 mo) | Placed **72.37%**
* **Band 4 (Ranks 76–100):** Avg Fees **₹6.75L** | Avg Salary **₹8.17 LPA** | Recovery **0.982 yrs** (11.8 mo) | Placed **64.27%**

### 3. State-Level Disparities
* **Top Performing States:** **West Bengal** (0.420 yrs avg ratio, ₹12.50 LPA salary), **Madhya Pradesh** (0.437 yrs), **Assam** (0.493 yrs), and **Delhi** (0.602 yrs avg ratio across 6 institutions with a national-high **₹16.08 LPA** average salary).
* **Lowest Value States:** **Uttarakhand** (1.889 yrs avg ratio, dragged down by UPES and Graphic Era) and **Karnataka** (1.339 yrs avg ratio, influenced by high private tuition at Manipal and RVCE).

---

## Deliverables Summary

| Deliverable | File / Path | Description |
| :--- | :--- | :--- |
| **Interactive Dashboard** | [`dashboard.html`](dashboard.html) | Standalone interactive UI with Tailwind CSS, Chart.js, bubble scatter plot, rank band bar charts, state breakdown, and searchable college explorer. |
| **One-Page Insight Memo** | [`INSIGHT_MEMO.md`](INSIGHT_MEMO.md) | Formatted briefing memo answering the stakeholder's dilemma with 3 numerical insights, 1 decision rule, and honest data limits. |
| **Jupyter Notebook** | [`analysis_walkthrough.ipynb`](analysis_walkthrough.ipynb) | Reproducible walkthrough with formulas, aggregations, and tables. |
| **Merged Dataset** | [`colleges_final.csv`](colleges_final.csv) | Master table joining NIRF placement data with audited 4-year academic fees across all 100 institutions. |
| **Fee Audit & Sources** | [`fee_sources.md`](fee_sources.md) | Comprehensive 23 KB source-cited reference log for every institution's fee calculation. |

---

## Repository Architecture & Pipeline

```text
NIRF_Ranking_Analytics/
├── nirf_pipeline.py              # Automated downloader & NIRF DCS PDF parser (100 colleges)
├── build_final_artifacts.py      # Fee dictionary compiler, LEFT JOIN & audit generator
├── run_analytics.py              # Statistical aggregations across cohort, bands & states
├── generate_dashboard.py         # Compiles analytics into standalone dashboard.html
├── fee_dict_iits.py              # Audited fee structures: 22 IITs
├── fee_dict_nits.py              # Audited fee structures: 23 NITs
├── fee_dict_univ_state_govt.py   # Audited fee structures: 20 Central/State Universities
├── fee_dict_private_deemed.py    # Audited fee structures: 35 Private/Deemed Institutions
├── colleges_final.csv            # Master clean merged dataset (100 institutions)
├── college_fees_clean.csv        # Standardized 4-year academic fee table
├── college_fees_raw.csv          # Granular fee component breakdown
├── colleges_clean.csv            # Cleaned NIRF placement dataset (97 eligible + 3 PG-only)
├── fee_extraction_issues.csv     # Traceability log for PG-only non-eligible institutes
├── dashboard.html                # Interactive visual dashboard
├── INSIGHT_MEMO.md               # 1-page executive insight memo
├── fee_sources.md                # Source URLs and official circular references
└── analysis_walkthrough.ipynb    # Python walkthrough notebook
```

---

## How the Hardest Data Problem Was Solved

### The Problem
The official NIRF Data Capture System (DCS) PDFs publish detailed student intake, graduating counts, campus placement numbers, and capital/operational expenditures—**but completely omit student tuition and academic fees**.

### The Solution
1. **Automated NIRF Pipeline:** Built an automated Python pipeline using `urllib` and `pypdf` to download all 100 institutional PDFs concurrently in 29.6 seconds without manual intervention.
2. **Audited Fee Data Collection:** Collected and standardized four-year mandatory academic fees for all 100 institutions using a strict hierarchy:
   - *Tier 1 (IITs & NITs):* MHRD/MoE statutory tuition fee notifications (₹8.0L for IITs, ₹5.0L for NITs) + audited mandatory institute dues.
   - *Tier 2 (Central/State Universities):* Official university admission bulletins (e.g., JAC Delhi, WBJEE, TNEA).
   - *Tier 3 (Private/Deemed Universities):* Official institutional fee circulars, prospectuses, and approved fee regulatory committee notifications.
3. **Strict Data Integrity:**
   - Preserved all 100 original institutions (zero row loss).
   - Flagged 3 postgraduate-only institutions (`IIIT Bangalore`, `Univ of Hyderabad`, `DIAT Pune`) as `vfm_eligible=False` without fabricating data.
   - Asserted unique institute IDs and numeric boundaries across all pipeline stages.

---

## Quickstart & Reproducibility

To reproduce the entire pipeline from scratch:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd NIRF_Ranking_Analytics

# 2. Run data extraction and PDF parsing (downloads original NIRF DCS PDFs)
python nirf_pipeline.py

# 3. Compile audited fee structures and merge datasets
python build_final_artifacts.py

# 4. Run analytics and compute cohort metrics
python run_analytics.py

# 5. Generate interactive dashboard
python generate_dashboard.py

# 6. Open dashboard in your default browser
# Windows:
start dashboard.html
# macOS:
open dashboard.html
# Linux:
xdg-open dashboard.html
```

---

## Honest Analytical Limitations ("What the Data Cannot Tell You")

1. **Branch Dispersion Masked by Median:** Institutional medians combine Computer Science salaries (often ₹18–₹25 LPA) with core branches (Civil/Mechanical/Chemical at ₹5–₹7 LPA).
2. **The Non-Placed Cohort (0 LPA):** NIRF median salary accounts *only* for students placed through campus interviews. Colleges with low placement percentages (e.g., KIIT at 34.9% or Vignan's at 43.4%) leave over half the graduating class with ₹0 initial campus earnings.
3. **Non-Academic Living Costs:** Mandatory hostel, mess, and living expenses add **₹1.2L to ₹2.2L per year** (₹4.8L to ₹8.8L over 4 years), which significantly increases total financial commitment beyond tuition fees alone.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.  
Academic data sources belong to the Ministry of Education (NIRF) and respective universities.
