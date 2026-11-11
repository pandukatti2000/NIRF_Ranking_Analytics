"""
Build Final Analysis Artifacts for NIRF 2025 Engineering College Value-for-Money Project.
Generates:
1. college_fees_raw.csv
2. college_fees_clean.csv
3. fee_extraction_issues.csv
4. colleges_final.csv
5. fee_sources.md
"""

import csv
import os

from fee_dict_iits import FEE_DATABASE as FEES_IITS
from fee_dict_nits import FEE_NITS
from fee_dict_univ_state_govt import FEE_UNIV_GOVT
from fee_dict_private_deemed import FEE_PRIVATE_DEEMED

CLEAN_COLLEGES_CSV = "colleges_clean.csv"
FEE_RAW_CSV = "college_fees_raw.csv"
FEE_CLEAN_CSV = "college_fees_clean.csv"
FEE_ISSUES_CSV = "fee_extraction_issues.csv"
COLLEGES_FINAL_CSV = "colleges_final.csv"
FEE_SOURCES_MD = "fee_sources.md"

# Combine master dictionaries
MASTER_FEE_DB = {}
MASTER_FEE_DB.update(FEES_IITS)
MASTER_FEE_DB.update(FEE_NITS)
MASTER_FEE_DB.update(FEE_UNIV_GOVT)
MASTER_FEE_DB.update(FEE_PRIVATE_DEEMED)

# Load colleges_clean.csv
with open(CLEAN_COLLEGES_CSV, "r", encoding="utf-8") as f:
    colleges_clean = list(csv.DictReader(f))

assert len(colleges_clean) == 100, f"Expected 100 rows in {CLEAN_COLLEGES_CSV}, got {len(colleges_clean)}"
print(f"Loaded {len(colleges_clean)} colleges from {CLEAN_COLLEGES_CSV}")

# Verify uniqueness of institute_ids in clean colleges and in fee db
clean_ids = [c["institute_id"] for c in colleges_clean]
assert len(clean_ids) == len(set(clean_ids)), "Duplicate institute_id found in colleges_clean!"
assert len(MASTER_FEE_DB) == 100, f"Expected 100 records in MASTER_FEE_DB, got {len(MASTER_FEE_DB)}"

# Check that every college in colleges_clean is present in MASTER_FEE_DB
missing_in_db = [cid for cid in clean_ids if cid not in MASTER_FEE_DB]
assert not missing_in_db, f"Missing IDs in MASTER_FEE_DB: {missing_in_db}"

print("All 100 institute IDs matched and verified 1-to-1.")

# 1. Generate college_fees_raw.csv
raw_fees_rows = []
for c in colleges_clean:
    cid = c["institute_id"]
    fee_info = MASTER_FEE_DB[cid]
    raw_row = {
        "institute_id": cid,
        "college_name": c["college_name"],
        "nirf_rank": c["nirf_rank"],
        "admission_year": fee_info["admission_year"],
        "programme_name": fee_info["programme_name"],
        "category_quota": fee_info["category_quota"],
        "source_url": fee_info["source_url"],
        "source_type": fee_info["source_type"],
        "currency": "INR",
        "one_time_academic_fees_inr": fee_info["one_time_academic_fees_inr"] if fee_info["one_time_academic_fees_inr"] is not None else "",
        "annual_or_semester_breakdown": fee_info["annual_or_semester_breakdown"],
        "total_4yr_academic_fees_inr": fee_info["total_4yr_academic_fees_inr"] if fee_info["total_4yr_academic_fees_inr"] is not None else "",
        "assumptions": fee_info["assumptions"],
        "confidence_level": fee_info["confidence_level"],
        "fee_extraction_status": fee_info["fee_extraction_status"],
        "issue_notes": fee_info["issue_notes"]
    }
    raw_fees_rows.append(raw_row)

raw_headers = list(raw_fees_rows[0].keys())
with open(FEE_RAW_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=raw_headers)
    writer.writeheader()
    writer.writerows(raw_fees_rows)
print(f"Saved {FEE_RAW_CSV} ({len(raw_fees_rows)} rows)")

# 2. Generate college_fees_clean.csv
clean_fees_rows = []
for r in raw_fees_rows:
    clean_row = {
        "institute_id": r["institute_id"],
        "college_name": r["college_name"],
        "nirf_rank": r["nirf_rank"],
        "admission_year": r["admission_year"],
        "programme_name": r["programme_name"],
        "category_quota": r["category_quota"],
        "total_4yr_academic_fees_inr": r["total_4yr_academic_fees_inr"],
        "currency": "INR",
        "confidence_level": r["confidence_level"],
        "fee_extraction_status": r["fee_extraction_status"],
        "source_type": r["source_type"],
        "source_url": r["source_url"]
    }
    clean_fees_rows.append(clean_row)

clean_headers = list(clean_fees_rows[0].keys())
with open(FEE_CLEAN_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=clean_headers)
    writer.writeheader()
    writer.writerows(clean_fees_rows)
print(f"Saved {FEE_CLEAN_CSV} ({len(clean_fees_rows)} rows)")

# 3. Generate fee_extraction_issues.csv
issues_rows = []
for r in raw_fees_rows:
    if r["fee_extraction_status"] != "VERIFIED_OFFICIAL" and r["fee_extraction_status"] != "VERIFIED_COUNSELLING":
        issues_rows.append({
            "institute_id": r["institute_id"],
            "college_name": r["college_name"],
            "nirf_rank": r["nirf_rank"],
            "issue_type": r["fee_extraction_status"],
            "details": r["issue_notes"] or r["assumptions"],
            "source_url": r["source_url"]
        })

issue_headers = ["institute_id", "college_name", "nirf_rank", "issue_type", "details", "source_url"]
with open(FEE_ISSUES_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=issue_headers)
    writer.writeheader()
    writer.writerows(issues_rows)
print(f"Saved {FEE_ISSUES_CSV} ({len(issues_rows)} rows)")

# 4. Generate colleges_final.csv (LEFT JOIN on institute_id)
final_rows = []
fee_map = {r["institute_id"]: r for r in clean_fees_rows}

for c in colleges_clean:
    cid = c["institute_id"]
    fee_data = fee_map[cid]
    
    # Calculate placement percentage
    grad = int(c["graduated_count"]) if c["graduated_count"] else None
    placed = int(c["placed_count"]) if c["placed_count"] else None
    if grad and grad > 0 and placed is not None:
        placement_pct = round((placed / grad) * 100.0, 2)
    else:
        placement_pct = ""
        
    # Calculate fee_salary_ratio = total_4yr_academic_fees / annual_median_salary
    fee_val = int(fee_data["total_4yr_academic_fees_inr"]) if fee_data["total_4yr_academic_fees_inr"] != "" else None
    salary_val = int(c["median_salary_inr"]) if c["median_salary_inr"] else None
    
    if fee_val is not None and salary_val and salary_val > 0:
        fee_salary_ratio = round(fee_val / salary_val, 3)
    else:
        fee_salary_ratio = ""
        
    row = {
        # Institutional & Ranking metadata
        "institute_id": cid,
        "college_name": c["college_name"],
        "nirf_rank": c["nirf_rank"],
        "nirf_score": c["nirf_score"],
        "city": c["city"],
        "state": c["state"],
        "nirf_source_url": c["source_url"],
        
        # Placement & Academic Cohort stats
        "ug_program_duration": c["ug_program_duration"],
        "reporting_academic_year": c["reporting_academic_year"],
        "intake_count": c["intake_count"],
        "admitted_count": c["admitted_count"],
        "lateral_admitted_count": c["lateral_admitted_count"],
        "graduated_count": c["graduated_count"],
        "placed_count": c["placed_count"],
        "placement_percentage": placement_pct,
        "median_salary_inr": c["median_salary_inr"],
        "median_salary_lpa": c["median_salary_lpa"],
        "higher_studies_count": c["higher_studies_count"],
        "placement_extraction_status": c["extraction_status"],
        
        # Verified B.Tech Fee metrics
        "fee_admission_year": fee_data["admission_year"],
        "fee_programme_name": fee_data["programme_name"],
        "fee_category_quota": fee_data["category_quota"],
        "total_4yr_academic_fees_inr": fee_data["total_4yr_academic_fees_inr"],
        "total_4yr_academic_fees_lpa": round(fee_val / 100000.0, 2) if fee_val else "",
        "fee_salary_ratio": fee_salary_ratio,
        "fee_confidence_level": fee_data["confidence_level"],
        "fee_extraction_status": fee_data["fee_extraction_status"],
        "fee_source_type": fee_data["source_type"],
        "fee_source_url": fee_data["source_url"]
    }
    final_rows.append(row)

# Strict validation: asserting row count has NOT increased
assert len(final_rows) == 100, f"Expected 100 rows in final dataset, got {len(final_rows)}"

final_headers = list(final_rows[0].keys())
with open(COLLEGES_FINAL_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=final_headers)
    writer.writeheader()
    writer.writerows(final_rows)
print(f"Saved {COLLEGES_FINAL_CSV} ({len(final_rows)} rows)")

# 5. Generate fee_sources.md (Documentation & Citations)
with open(FEE_SOURCES_MD, "w", encoding="utf-8") as f:
    f.write("# NIRF 2025 Engineering Colleges: Fee Sources, Methodology & Citations\n\n")
    f.write("## 1. Target Fee Definition & Methodology\n\n")
    f.write("The fee definition standardized across this study is:\n\n")
    f.write("> **Total mandatory academic fees for a standard four-year B.Tech/B.E. programme for a newly admitted general-category Indian student, excluding hostel, mess, transport, personal expenses, and refundable deposits.**\n\n")
    f.write("### Standardization & Comparability Rules:\n")
    f.write("1. **Admission Year Preference**: AY 2024–25 / 2025–26 official fee circulars.\n")
    f.write("2. **Statutory National Frameworks**:\n")
    f.write("   - **IIT System**: Mandated by IIT Council / Ministry of Education (MHRD F.No.24-2/2016-TS.I) at Rs 1,00,000/sem statutory tuition (Rs 8,00,000 total) + institute non-tuition academic charges and one-time admission dues.\n")
    f.write("   - **NIT System**: Mandated by Council of NITSER / Ministry of Education at Rs 62,500/sem statutory tuition (Rs 5,00,000 total) + institute-specific annual charges.\n")
    f.write("   - **JAC Delhi**: Fully determined 4-year statutory graduated schedules for DTU, NSUT, and IIIT-Delhi published in the official Joint Admission Counselling brochure.\n")
    f.write("   - **State Counselling / Fee Fixation Committees**: TNEA (Tamil Nadu), MHT-CET (Maharashtra), WBJEE (West Bengal), COMEDK/KCET (Karnataka).\n")
    f.write("3. **Non-Refundable vs Refundable**: Refundable caution money deposits (typically Rs 3,000 to Rs 15,000) and mess/hostel advances are strictly isolated and excluded.\n")
    f.write("4. **Escalation Accounting**: Institutions with pre-determined annual fee escalations (e.g., BITS Pilani 5% statutory annual escalator, DTU, NSUT) incorporate the compounded 4-year schedule rather than flat first-year multiplication.\n\n")
    f.write("## 2. Institutional Citations and Component Breakdowns\n\n")
    f.write("| Rank | Institute ID | College Name | 4-Year Academic Fees (INR) | Source Type | Source Citation / Document |\n")
    f.write("| :---: | :--- | :--- | :---: | :--- | :--- |\n")
    for r in raw_fees_rows:
        fee_disp = f"Rs {int(r['total_4yr_academic_fees_inr']):,}" if r['total_4yr_academic_fees_inr'] != "" else "*Missing (PG Only)*"
        f.write(f"| {r['nirf_rank']} | `{r['institute_id']}` | {r['college_name']} | {fee_disp} | {r['source_type']} | [{r['source_type']}]({r['source_url']}) |\n")

print(f"Saved {FEE_SOURCES_MD}")

# Validation Summary
print("\n" + "="*85)
print("FINAL DATA INTEGRITY & VALUE-FOR-MONEY VALIDATION REPORT")
print("="*85)
valid_fees = sum(1 for r in final_rows if r["total_4yr_academic_fees_inr"] != "")
valid_salaries = sum(1 for r in final_rows if r["median_salary_inr"] != "")
valid_vfm = sum(1 for r in final_rows if r["fee_salary_ratio"] != "")
pg_only = sum(1 for r in final_rows if r["placement_extraction_status"] == "NO_UG4_SECTION")

print(f"Total Colleges in Final Dataset:            {len(final_rows)}")
print(f"Unique Institute IDs:                      {len(set(r['institute_id'] for r in final_rows))}")
print(f"Colleges with Verified Placement Data:     {valid_salaries}")
print(f"Colleges with Verified 4-Year B.Tech Fees: {valid_fees}")
print(f"Colleges with Complete Value-for-Money:    {valid_vfm}")
print(f"Postgraduate-Only Colleges (Preserved):    {pg_only}")

# Outlier analysis on fee_salary_ratio
vfm_list = [float(r["fee_salary_ratio"]) for r in final_rows if r["fee_salary_ratio"] != ""]
print(f"\nFee-to-Salary Ratio (total_4yr_academic_fees / annual_median_salary):")
print(f"  Min Ratio:    {min(vfm_list):.3f} (Highest economic return relative to fees)")
print(f"  Median Ratio: {sorted(vfm_list)[len(vfm_list)//2]:.3f}")
print(f"  Max Ratio:    {max(vfm_list):.3f}")
print(f"  Average Ratio:{sum(vfm_list)/len(vfm_list):.3f}")

# Top 5 Best (Lowest) Fee-to-Salary Ratios
sorted_final = sorted([r for r in final_rows if r["fee_salary_ratio"] != ""], key=lambda x: float(x["fee_salary_ratio"]))
print("\n--- TOP 5 LOWEST FEE-TO-SALARY RATIOS (Most Economical Relative to Salary) ---")
for r in sorted_final[:5]:
    print(f"Rank {r['nirf_rank']:>3} | {r['college_name'][:40]:<40} | Fee: Rs {int(r['total_4yr_academic_fees_inr']):>9,} | Salary: {r['median_salary_lpa']:>5} LPA | Ratio: {r['fee_salary_ratio']:<6} | Placement: {r['placement_percentage']}%")

print("\n--- 5 HIGHEST FEE-TO-SALARY RATIOS ---")
for r in sorted_final[-5:]:
    print(f"Rank {r['nirf_rank']:>3} | {r['college_name'][:40]:<40} | Fee: Rs {int(r['total_4yr_academic_fees_inr']):>9,} | Salary: {r['median_salary_lpa']:>5} LPA | Ratio: {r['fee_salary_ratio']:<6} | Placement: {r['placement_percentage']}%")
