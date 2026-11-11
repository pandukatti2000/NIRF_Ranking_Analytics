# Demo Day Q&A Preparation Guide

**Project:** AccioJob DA-16 · Spin Build Pitch (Data Analytics)  
**Topic:** Value-for-Money Analysis of NIRF 2025 Engineering Colleges  
**Audience:** Technical Evaluators, Industry Mentors & Peer Reviewers  

---

## Question 1: How did you check the extracted numbers?

### The Core Answer:
> *"We implemented a dual-validation framework combining automated programmatic assertions with manual ground-truth auditing across both placement figures and academic fee calculations."*

### Detailed Technical Points:
1. **Automated Pipeline Audits (`nirf_pipeline.py` & `validate_data.py`):**
   - **Unique Key Integrity:** Asserted strictly that all 100 institute IDs (`IR-E-...`) are unique across all pipeline stages, preventing cross-row contamination or accidental duplication during merges.
   - **Schema & Type Enforcement:** Automated regex checks verified that student counts (`graduated_students`, `placed_students`, `higher_studies`) are non-negative integers where $\text{placed} + \text{higher\_studies} \le \text{graduated}$.
   - **Salary Range Boundaries:** Validated that median salaries fell within realistic market ranges (₹3,00,000 to ₹35,00,000). Identified and flagged 3 institutions with no 4-year undergraduate intake (`IIIT Bangalore`, `Univ of Hyderabad`, `DIAT Pune`), isolating them to prevent metric skew.
2. **Manual Ground-Truth Auditing (Spot-Checking):**
   - **NIRF Placement Data:** Manually verified 10 diverse college DCS PDFs directly against our extracted CSVs (e.g., IIT Madras, IIT Bombay, Jadavpur University, COEP Pune, DTU Delhi, VIT Vellore). Confirmed table row matches for `UG [4 Years Program(s)]` academic year `2023-24`.
   - **Fee Data Traceability:** Because NIRF DCS files omit student tuition fees, we extracted fee schedules exclusively from official notifications:
     - *IITs (22 institutions):* Verified statutory council cap of ₹1,00,000/semester tuition (₹8.0 Lakhs 4-year tuition) + audited one-time institute admission dues and recurring amenities fees (e.g., IIT Bombay total academic ₹8.83L; IIT Madras ₹8.85L).
     - *NITs (23 institutions):* Verified statutory cap of ₹62,500/semester tuition (₹5.0 Lakhs 4-year tuition) + audited student activity, exam, and registration charges (e.g., NIT Trichy ₹5.84L; NIT Surathkal ₹6.04L).
     - *State Universities & Private Colleges (52 institutions):* Pulled directly from official 2024–25 / 2025–26 fee circulars (e.g., Jadavpur Information Brochure: ₹2,400 annual tuition + ₹4,510 first-year dues = ₹14,110; SRM Information Brochure: Category 1 ₹4,50,000/yr = ₹18.10L).
   - **Transparent Citation Log:** Every single rupee is documented with URL, admission year, quota, and breakdown in `fee_sources.md`.

---

## Question 2: Why that value metric?

### The Core Answer:
> *"We chose the **Fee-to-Salary Ratio** (Total 4-Year Academic Fees divided by Annual Median Placement Salary) because it directly translates financial risk into an intuitive, comparable unit of time—years of gross salary required to recover upfront educational costs—without making dangerous financial assumptions."*

### Detailed Technical Points:
1. **Why not ROI (Return on Investment %)?**
   - Standard ROI formulas require calculating the Present Value (PV) of discounted lifetime earnings over 20–30 years. Doing so requires fabricating dozens of arbitrary assumptions: future salary growth rates, inflation, discount rates, tax brackets, and job switching intervals.
   - The **Fee-to-Salary Ratio** avoids speculation. It compares verifiable current cash outlays against verified year-one exit earnings.
2. **Why not Net Payback Period?**
   - True payback period requires net disposable income after federal taxes, PF deductions, rent, groceries, and living expenses. Because cost-of-living varies drastically between posting locations (e.g., Bengaluru vs Coimbatore), calculating net payback introduces unverified regional cost assumptions.
   - We clearly explain that **0.9 years gross ratio does not mean 11 months in real life**; accounting for taxes and living expenses (saving ~30–40% of gross pay), actual recovery requires roughly $2.5\times$ to $3\times$ the ratio.
3. **Fairness Across Tiers:**
   - A college charging ₹20 Lakhs with an ₹8 LPA salary yields a ratio of **2.50 years**. A college charging ₹2 Lakhs with a ₹6 LPA salary yields a ratio of **0.33 years**. This metric immediately cuts through marketing hype to highlight educational efficiency.

---

## Question 3: What does median salary hide?

### The Core Answer:
> *"The median placement salary is an essential baseline, but it systematically hides three critical realities: branch-wise dispersion, zero-earning non-placed students, and living expense burdens."*

### Detailed Technical Points:
1. **Branch-Level Bimodal Disparities (The CS/IT vs Core Split):**
   - NIRF aggregates all engineering branches into a single institutional median. In institutions like DTU or NIT Trichy, Computer Science and IT students frequently secure median packages of ₹20–₹26 LPA, while Civil, Environmental, Production, or Metallurgy graduates receive offers closer to ₹6–₹8 LPA.
   - A single institutional median gives core engineering students a false sense of security regarding their expected financial recovery timeline.
2. **The Non-Placed Denominator Effect (The 0 LPA Cohort):**
   - NIRF calculates median salary **exclusively for students who received placement offers**. It ignores students who graduated but remained unemployed.
   - For example, in colleges with high placement rates like IIT Patna (95.5%) or Jadavpur (91.0%), the median salary accurately represents the vast majority of graduating students.
   - However, in institutions with low placement rates like KIIT (34.9% placed) or Vignan's (43.4% placed), over 55% to 65% of the graduating cohort earned **₹0** from campus placements. The reported median salary applies only to the fortunate minority.
3. **Fixed Campus Overhead vs Tuition:**
   - The median salary compares only against mandatory academic fees. In residential institutions, mandatory food and lodging costs add ₹1.2L to ₹2.2L per year (₹4.8L to ₹8.8L over 4 years).
   - In ultra-low-fee colleges like Jadavpur, living expenses represent >90% of the true cost of attendance. In private colleges, living costs push total capital investment beyond ₹25 Lakhs.
