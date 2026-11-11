import csv
import re
from pypdf import PdfReader

CLEAN_CSV = "colleges_clean.csv"

with open(CLEAN_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in {CLEAN_CSV}: {len(rows)}")

# 1. Unique Institute IDs
ids = [r["institute_id"] for r in rows]
unique_ids = set(ids)
print(f"Unique Institute IDs: {len(unique_ids)} / {len(rows)}")
assert len(unique_ids) == len(rows), "Duplicate Institute IDs found!"

# 2. Check ranks
ranks = [int(r["nirf_rank"]) for r in rows]
print(f"Ranks min: {min(ranks)}, max: {max(ranks)}, unique: {len(set(ranks))}")

# 3. Check scores
scores = [float(r["nirf_score"]) for r in rows if r["nirf_score"]]
print(f"Scores min: {min(scores)}, max: {max(scores)}")

# 4. Check placement and graduation consistency
issues = []
for r in rows:
    if r["extraction_status"] == "SUCCESS":
        grad = int(r["graduated_count"])
        placed = int(r["placed_count"])
        salary = int(r["median_salary_inr"])
        
        # Placed cannot exceed graduated
        if placed > grad:
            issues.append(f"Rank {r['nirf_rank']} {r['college_name']}: Placed ({placed}) > Graduated ({grad})")
            
        # Salary sanity check (between 2 LPA and 50 LPA)
        if salary < 200000 or salary > 50000000:
            issues.append(f"Rank {r['nirf_rank']} {r['college_name']}: Suspicious salary {salary}")

print(f"Logic anomalies found: {len(issues)}")
for iss in issues:
    print("  ", iss)

# 5. Outlier Analysis
successful_rows = [r for r in rows if r["extraction_status"] == "SUCCESS"]
sorted_by_salary = sorted(successful_rows, key=lambda x: float(x["median_salary_lpa"]), reverse=True)

print("\n--- TOP 5 HIGHEST MEDIAN SALARIES ---")
for r in sorted_by_salary[:5]:
    print(f"Rank {r['nirf_rank']:>3} | {r['college_name'][:40]:<40} | Salary: {r['median_salary_lpa']:>6} LPA | Placed: {r['placed_count']:>4}/{r['graduated_count']:<4}")

print("\n--- 5 LOWEST MEDIAN SALARIES ---")
for r in sorted_by_salary[-5:]:
    print(f"Rank {r['nirf_rank']:>3} | {r['college_name'][:40]:<40} | Salary: {r['median_salary_lpa']:>6} LPA | Placed: {r['placed_count']:>4}/{r['graduated_count']:<4}")

# 6. Manual inspection of 5 diverse colleges:
# Rank 10, Rank 25, Rank 50, Rank 75, Rank 100
sample_ranks = ["10", "25", "50", "75", "100"]
print("\n" + "="*80)
print("MANUAL VERIFICATION OF 5 DIVERSE COLLEGES AGAINST ORIGINAL PDF")
print("="*80)

for target_rank in sample_ranks:
    r = next(item for item in rows if item["nirf_rank"] == target_rank)
    inst_id = r["institute_id"]
    pdf_path = f"downloads/{inst_id}.pdf"
    
    # Read raw PDF text
    reader = PdfReader(pdf_path)
    full_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    
    # Find the UG4 section
    match = re.search(r'UG\s*\[4\s*Years\s*Program\(s\)\]:\s*Placement.*?(?:2023-24.*?\n)', full_text, re.DOTALL | re.IGNORECASE)
    pdf_snippet = match.group(0).strip().split("\n")[-1] if match else "Snippet not matched"
    
    print(f"\n--- Rank {target_rank}: {r['college_name']} ({inst_id}) ---")
    print(f"Extracted CSV: Graduated={r['graduated_count']}, Placed={r['placed_count']}, Median Salary={r['median_salary_inr']} ({r['median_salary_lpa']} LPA), Higher Studies={r['higher_studies_count']}")
    print(f"Raw PDF Line:  {pdf_snippet}")
