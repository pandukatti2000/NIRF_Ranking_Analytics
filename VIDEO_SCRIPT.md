# 2-Minute Video Presentation Script: "Is That College Worth the Fees?"

**Project:** AccioJob DA-16 · Spin Build Pitch (Data Analytics)  
**Presenter:** Data Analyst / Engineer  
**Target Duration:** Exactly 120 seconds (2 minutes)  
**Deliverable Type:** Word-for-word spoken pitch with second-by-second timestamps and screen cues.

---

## Script Breakdown & Spoken Dialogue

### [0:00 – 0:15] The Hook: The High-Stakes Decision
* **Visual on Screen:** Opening slide showing the title, followed immediately by a screen recording showing the interactive dashboard at `dashboard.html`.
* **Presenter Spoken Dialogue (15 seconds · ~38 words):**  
  > *"Every year, over a million Indian families take on crushing student loans to send their child to an engineering college, assuming that a higher NIRF rank guarantees a great return. But does it? Today, we answer one crucial question: **Which college actually gives you the best return for the fees you pay?**"*

---

### [0:15 – 1:15] The Dashboard Walkthrough: Real Numbers & Revelations
* **Visual on Screen:** Zoom in on the KPI summary banner (97 eligible colleges, ₹8.43L average fee, ₹11.14 LPA median salary, 0.904 years recovery). Then switch to the interactive Scatter Plot and Top 10 Value cards.
* **Presenter Spoken Dialogue (60 seconds · ~145 words):**  
  > *"To answer this, we analyzed all 100 top NIRF 2025 engineering colleges using a simple metric: **Fee-to-Salary Ratio**—the number of years of gross median salary needed to recover your 4-year academic fees.*  
  >  
  > *Look at our dashboard. The cohort average recovery time is **0.9 years**—about 11 months. But the variation is astonishing.*  
  >  
  > *In our top 10 best-value colleges, public institutions dominate. **Jadavpur University** in West Bengal charges just **₹14,110** total academic fees for 4 years against a **₹10.5 LPA** median salary. That's a recovery ratio of **0.013 years**—less than one week of salary! Similarly, **Jamia Millia Islamia** costs **₹66,000** for a **₹13.8 LPA** salary—recovered in just 18 days.*  
  >  
  > *Now look at the worst-value quadrant. High-fee private universities charge up to **₹18 to ₹20 Lakhs** for median salaries of only **₹5 to ₹6.5 LPA**. **SRM IST** at rank 14 charges **₹18.1 Lakhs** for a **₹6.2 LPA** salary—taking **2.92 years** of gross salary to recover. That is **224 times longer** than Jadavpur!*  
  >  
  > *And looking across rank bands: Rank Band 2 and 3 colleges actually charge **higher** average fees than Band 1—over **₹9.1 Lakhs**—while delivering **29% lower** median salaries."*

---

### [1:15 – 1:45] Methodology & The Hardest Data Problem Solved
* **Visual on Screen:** Transition to the data pipeline diagram, CSV tables (`colleges_final.csv`, `college_fees_clean.csv`), and the NIRF PDF downloads folder.
* **Presenter Spoken Dialogue (30 seconds · ~75 words):**  
  > *"How did we build this? NIRF's institutional data files publish UG 4-year placement numbers and expenditures, but they **completely omit** student tuition fees.*  
  >  
  > *That was our hardest data engineering hurdle: we couldn't invent numbers or scrape third-party blogs. We built a reproducible Python pipeline that downloaded all 100 official NIRF PDFs, parsed the exact graduating 2020–24 cohorts, and cross-referenced 100 official institutional fee schedules, JoSAA circulars, and university notifications to calculate audited 4-year academic dues. Every single rupee is source-cited."*

---

### [1:45 – 2:00] Strategic Recommendation & Data Limitations
* **Visual on Screen:** Return to the dashboard summary and display the final Decision Rule card.
* **Presenter Spoken Dialogue (15 seconds · ~42 words):**  
  > *"Our recommendation to parents: Prioritize premier state universities and subsidized CFTIs over private universities ranked 26 to 75. But remember: campus median salaries hide branch spreads, and living costs add ₹5 to ₹8 Lakhs. Check the dashboard, explore your state, and make an informed choice!"*

---

## Timing & Pacing Checklist for Recording

| Time Bracket | Target Word Count | Section | Key Visual Cue |
| :--- | :---: | :--- | :--- |
| **0:00 – 0:15** | 38 words | The Hook & Stakeholder Framing | Title Card & Dashboard Overview |
| **0:15 – 1:15** | 145 words | Dashboard Walkthrough (Best vs Worst, Bands) | Scatter Plot, Jadavpur vs SRM, Rank Bands |
| **1:15 – 1:45** | 75 words | Methodology & Hardest Problem (Fee Omission) | Python Pipeline & Source Audits |
| **1:45 – 2:00** | 42 words | Clear Recommendation & Honest Limits | Final Decision Matrix & Call to Action |
| **Total** | **300 words** | **Paced at ~150 words per minute (natural speaking pace)** | **Strict 120-second cap** |
