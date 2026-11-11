"""
NIRF 2025 Engineering Rankings Data Pipeline
Scalable, reproducible pipeline to extract NIRF 2025 engineering college data
and institute DCS PDF placement statistics with bounded concurrency, retries, and caching.
"""

import os
import re
import csv
import sys
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

BASE_URL = "https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html"
CDN_BASE = "https://www.nirfindia.org/nirfpdfcdn/2025/pdf/Engineering/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

DOWNLOAD_DIR = "downloads"
RAW_CSV = "colleges_raw.csv"
CLEAN_CSV = "colleges_clean.csv"
ISSUES_CSV = "extraction_issues.csv"

CSV_FIELDS = [
    "institute_id",
    "college_name",
    "nirf_rank",
    "nirf_score",
    "city",
    "state",
    "source_url",
    "ug_program_duration",
    "reporting_academic_year",
    "intake_count",
    "admitted_count",
    "lateral_admitted_count",
    "graduated_count",
    "placed_count",
    "median_salary_inr",
    "median_salary_lpa",
    "higher_studies_count",
    "ug_programme_fee_inr",
    "fee_status",
    "extraction_status",
    "extraction_notes"
]

def fetch_ranking_page(cache_file="page_2025.html"):
    """Fetches the official NIRF rankings page or loads from local cache."""
    if os.path.exists(cache_file):
        print(f"[CACHE] Loading rankings HTML from local cache: {cache_file}", flush=True)
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
            
    print(f"[FETCH] Downloading rankings HTML from {BASE_URL}...", flush=True)
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=25)
    resp.raise_for_status()
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"[CACHE] Saved rankings HTML to {cache_file} ({len(resp.content)} bytes)", flush=True)
    return resp.text

def parse_ranking_rows(html_content, limit=None):
    """Parses institute rows from the ranking table."""
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", id="tbl_overall")
    if not table:
        raise ValueError("Could not find ranking table '#tbl_overall' in HTML.")
        
    tbody = table.find("tbody")
    rows = tbody.find_all("tr", recursive=False) if tbody else table.find_all("tr")
    
    colleges = []
    for r in rows:
        tds = r.find_all("td", recursive=False)
        if len(tds) < 6:
            continue
            
        inst_id = tds[0].get_text(strip=True)
        raw_name = tds[1].get_text(" ", strip=True)
        # Clean button labels like 'More Details', 'Close', '||'
        name = re.split(r'More Details|Close|\|\|', raw_name)[0].strip()
        name = re.sub(r'\s+', ' ', name)
        
        city = tds[2].get_text(strip=True)
        state = tds[3].get_text(strip=True)
        score_str = tds[4].get_text(strip=True)
        rank_str = tds[5].get_text(strip=True)
        
        # Locate PDF anchor
        pdf_url = None
        for a in tds[1].find_all("a"):
            href = a.get("href", "")
            if href and href.endswith(".pdf"):
                pdf_url = href
                break
                
        if not pdf_url and inst_id:
            pdf_url = f"{CDN_BASE}{inst_id}.pdf"
            
        colleges.append({
            "institute_id": inst_id,
            "college_name": name,
            "city": city,
            "state": state,
            "nirf_score": score_str,
            "nirf_rank": rank_str,
            "source_url": pdf_url
        })
        
        if limit and len(colleges) >= limit:
            break
            
    return colleges

def download_single_pdf(college, max_retries=3, delay=0.2):
    """Downloads a single institute PDF with retries and caching."""
    inst_id = college["institute_id"]
    pdf_url = college["source_url"]
    save_path = os.path.join(DOWNLOAD_DIR, f"{inst_id}.pdf")
    
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
        return inst_id, True, "CACHED", save_path
        
    for attempt in range(1, max_retries + 1):
        try:
            time.sleep(delay)
            resp = requests.get(pdf_url, headers=HEADERS, timeout=25)
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return inst_id, True, "DOWNLOADED", save_path
            elif resp.status_code == 404:
                return inst_id, False, "HTTP_404_NOT_FOUND", save_path
            else:
                if attempt == max_retries:
                    return inst_id, False, f"HTTP_{resp.status_code}", save_path
        except Exception as e:
            if attempt == max_retries:
                return inst_id, False, f"EXCEPTION: {str(e)[:40]}", save_path
        time.sleep(0.5 * attempt)
        
    return inst_id, False, "UNKNOWN_ERROR", save_path

def download_all_pdfs(colleges, max_workers=5):
    """Downloads PDFs concurrently using bounded ThreadPoolExecutor."""
    print(f"\n[DOWNLOAD] Starting bounded download pool (max_workers={max_workers})...", flush=True)
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_col = {executor.submit(download_single_pdf, c): c for c in colleges}
        completed = 0
        for future in as_completed(future_to_col):
            c = future_to_col[future]
            completed += 1
            inst_id, success, msg, path = future.result()
            results[inst_id] = (success, msg, path)
            if completed % 20 == 0 or completed == len(colleges):
                print(f"[DOWNLOAD] Progress: {completed}/{len(colleges)} PDFs processed.", flush=True)
    return results

def extract_pdf_data(pdf_path):
    """Extracts placement statistics and verifies fee availability in PDF."""
    result = {
        "ug_program_duration": "UG [4 Years Program(s)]",
        "reporting_academic_year": "2023-24",
        "intake_count": "",
        "admitted_count": "",
        "lateral_admitted_count": "",
        "graduated_count": "",
        "placed_count": "",
        "median_salary_inr": "",
        "median_salary_lpa": "",
        "higher_studies_count": "",
        "ug_programme_fee_inr": "",  # Explicitly empty / missing per NIRF design
        "fee_status": "NOT_REPORTED_BY_NIRF",
        "extraction_status": "PENDING",
        "extraction_notes": ""
    }
    
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 1000:
        result["extraction_status"] = "PDF_NOT_FOUND"
        result["extraction_notes"] = "PDF file could not be downloaded or was invalid."
        return result
        
    try:
        reader = PdfReader(pdf_path)
        full_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        result["extraction_status"] = "PDF_CORRUPT_OR_UNREADABLE"
        result["extraction_notes"] = f"PdfReader exception: {str(e)[:50]}"
        return result

    # Check for tuition fee reporting in DCS
    # (NIRF DCS reports student counts receiving fee reimbursements, not student tuition fees)
    fee_match = re.search(r'(?:tuition\s*fee|total\s*fee|programme\s*fee|annual\s*fee)[\s:]*(?:Rs\.?|INR)?\s*([0-9,]+)', full_text, re.IGNORECASE)
    if fee_match:
        result["ug_programme_fee_inr"] = fee_match.group(1).replace(",", "")
        result["fee_status"] = "PRESENT"
    else:
        result["ug_programme_fee_inr"] = ""
        result["fee_status"] = "NOT_REPORTED_BY_NIRF"

    # Extract UG 4 Years Placement Section
    pattern = r'UG\s*\[4\s*Years\s*Program\(s\)\]:\s*Placement\s*&\s*higher\s*studies\s*for\s*previous\s*3\s*years(.*?)(?:UG\s*\[5|PG\s*\[|Ph\.D|Financial\s*Resources)'
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    
    if not match:
        # Check if institute has other UG programs (e.g. 5-year only or PG only)
        if "UG [5 Years" in full_text:
            result["ug_program_duration"] = "UG [5 Years Program(s)] ONLY"
            result["extraction_status"] = "NO_UG4_SECTION"
            result["extraction_notes"] = "Institute does not offer 4-year UG program (offers 5-year UG)."
        elif "PG [" in full_text:
            result["ug_program_duration"] = "PG ONLY"
            result["extraction_status"] = "NO_UG4_SECTION"
            result["extraction_notes"] = "Institute is postgraduate only; no UG program found."
        else:
            result["extraction_status"] = "NO_UG4_SECTION"
            result["extraction_notes"] = "No UG [4 Years Program(s)] placement section found in PDF."
        return result
        
    ug_section = match.group(1)
    
    # Method 1: Standard NIRF row pattern
    row_pattern = re.compile(
        r'(\d{4}-\d{2})\s+(\d+)\s+(\d+)\s+'           # Intake year, intake, admitted
        r'(\d{4}-\d{2})\s+(\d+)\s+'                   # Lateral year, lateral admitted
        r'(\d{4}-\d{2})\s+(\d+)\s+(\d+)\s+'           # Graduating year, graduated, placed
        r'(\d+)\s*\([^)]*\)\s*'                       # Median salary: numeric amount + text in parentheses
        r'(\d+)',                                     # Higher studies count
        re.DOTALL
    )
    matches = row_pattern.findall(ug_section)
    
    if matches:
        target_row = None
        for m in matches:
            if m[5] == "2023-24":
                target_row = m
                break
        if not target_row:
            target_row = matches[-1]
            
        intake_yr, intake, admitted, lat_yr, lat_admitted, grad_yr, graduated, placed, median_salary, higher_studies = target_row
        
        result["reporting_academic_year"] = grad_yr
        result["intake_count"] = int(intake)
        result["admitted_count"] = int(admitted)
        result["lateral_admitted_count"] = int(lat_admitted)
        result["graduated_count"] = int(graduated)
        result["placed_count"] = int(placed)
        result["median_salary_inr"] = int(median_salary)
        result["median_salary_lpa"] = round(int(median_salary) / 100000.0, 2)
        result["higher_studies_count"] = int(higher_studies)
        result["extraction_status"] = "SUCCESS"
        result["extraction_notes"] = f"Extracted cohort graduating in {grad_yr}."
        return result

    # Method 2: Fallback pattern matching graduating year 2023-24
    alt_pattern = re.compile(
        r'(2023-24)\s+(\d+)\s+(\d+)\s+(\d+)\s*\(',
        re.DOTALL
    )
    alt_match = alt_pattern.search(ug_section)
    if alt_match:
        grad_yr, graduated, placed, median_salary = alt_match.groups()
        result["reporting_academic_year"] = grad_yr
        result["graduated_count"] = int(graduated)
        result["placed_count"] = int(placed)
        result["median_salary_inr"] = int(median_salary)
        result["median_salary_lpa"] = round(int(median_salary) / 100000.0, 2)
        result["extraction_status"] = "PARTIAL_SUCCESS"
        result["extraction_notes"] = "Extracted placement and salary via fallback pattern; intake/lateral counts omitted."
        return result

    # Method 3: Line tokenization fallback
    lines = [l.strip() for l in ug_section.split("\n") if l.strip()]
    for idx_l, line in enumerate(lines):
        if "2023-24" in line:
            # Check numbers in current and following lines
            combined_window = " ".join(lines[max(0, idx_l-2):min(len(lines), idx_l+5)])
            nums = re.findall(r'\b\d+\b', combined_window)
            # Find salary pattern like 500000 or 1200000
            salary_cand = [int(n) for n in nums if len(n) >= 5 and int(n) >= 100000 and int(n) <= 50000000]
            if salary_cand:
                result["reporting_academic_year"] = "2023-24"
                result["median_salary_inr"] = salary_cand[0]
                result["median_salary_lpa"] = round(salary_cand[0] / 100000.0, 2)
                result["extraction_status"] = "PARTIAL_SUCCESS"
                result["extraction_notes"] = "Extracted median salary via token window fallback."
                return result

    result["extraction_status"] = "ROW_PARSE_FAILURE"
    result["extraction_notes"] = "UG 4-year section found but table rows could not be matched with regex."
    return result

def run_pipeline(limit=100, max_workers=5):
    """Executes the pipeline for a specified number of colleges."""
    start_time = time.time()
    print("=" * 85, flush=True)
    print(f"NIRF 2025 ENGINEERING DATA PIPELINE: SCALING TO {limit} COLLEGES", flush=True)
    print("=" * 85, flush=True)
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    html_content = fetch_ranking_page()
    colleges = parse_ranking_rows(html_content, limit=limit)
    print(f"Extracted {len(colleges)} college records from ranking table.\n", flush=True)
    
    # Step 1: Download all PDFs concurrently with caching
    download_results = download_all_pdfs(colleges, max_workers=max_workers)
    
    # Step 2: Extract data from each college and PDF sequentially for deterministic processing
    print(f"\n[PARSE] Extracting placement data from {len(colleges)} institute PDFs...", flush=True)
    raw_records = []
    issues = []
    
    for idx, c in enumerate(colleges, 1):
        inst_id = c["institute_id"]
        rank = c["nirf_rank"]
        name = c["college_name"]
        pdf_url = c["source_url"]
        
        dl_success, dl_msg, pdf_path = download_results.get(inst_id, (False, "NOT_IN_RESULTS", ""))
        
        if dl_success:
            pdf_data = extract_pdf_data(pdf_path)
        else:
            pdf_data = {
                "ug_program_duration": "UG [4 Years Program(s)]",
                "reporting_academic_year": "2023-24",
                "intake_count": "",
                "admitted_count": "",
                "lateral_admitted_count": "",
                "graduated_count": "",
                "placed_count": "",
                "median_salary_inr": "",
                "median_salary_lpa": "",
                "higher_studies_count": "",
                "ug_programme_fee_inr": "",
                "fee_status": "DOWNLOAD_FAILED",
                "extraction_status": "DOWNLOAD_FAILED",
                "extraction_notes": dl_msg
            }
            issues.append({
                "institute_id": inst_id,
                "college_name": name,
                "issue_type": "DOWNLOAD_FAILED",
                "details": dl_msg,
                "source_url": pdf_url
            })
            
        record = {**c, **pdf_data}
        raw_records.append(record)
        
        if pdf_data["extraction_status"] != "SUCCESS":
            issues.append({
                "institute_id": inst_id,
                "college_name": name,
                "issue_type": pdf_data["extraction_status"],
                "details": pdf_data["extraction_notes"],
                "source_url": pdf_url
            })
            
    # Save raw CSV
    with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(raw_records)
    print(f"\n[OUTPUT] Saved raw dataset: {RAW_CSV} ({len(raw_records)} records)", flush=True)
    
    # Save issues CSV
    issue_fields = ["institute_id", "college_name", "issue_type", "details", "source_url"]
    with open(ISSUES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=issue_fields)
        writer.writeheader()
        writer.writerows(issues)
    print(f"[OUTPUT] Saved issues log: {ISSUES_CSV} ({len(issues)} records)", flush=True)
    
    # Clean and validate records
    clean_records = []
    for r in raw_records:
        clean_row = dict(r)
        for num_field in ["intake_count", "admitted_count", "lateral_admitted_count", "graduated_count", "placed_count", "median_salary_inr", "higher_studies_count"]:
            val = clean_row.get(num_field, "")
            if val != "" and val is not None:
                try:
                    clean_row[num_field] = int(val)
                except ValueError:
                    clean_row[num_field] = ""
                    
        for float_field in ["nirf_score", "median_salary_lpa"]:
            val = clean_row.get(float_field, "")
            if val != "" and val is not None:
                try:
                    clean_row[float_field] = float(val)
                except ValueError:
                    clean_row[float_field] = ""
                    
        clean_records.append(clean_row)
        
    with open(CLEAN_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(clean_records)
    print(f"[OUTPUT] Saved clean dataset: {CLEAN_CSV} ({len(clean_records)} records)", flush=True)
    
    # Validation & Summary statistics
    total_eval = len(clean_records)
    unique_ids = len(set(r["institute_id"] for r in clean_records))
    success_count = sum(1 for r in clean_records if r["extraction_status"] == "SUCCESS")
    partial_count = sum(1 for r in clean_records if r["extraction_status"] == "PARTIAL_SUCCESS")
    no_ug4_count = sum(1 for r in clean_records if r["extraction_status"] == "NO_UG4_SECTION")
    failed_count = sum(1 for r in clean_records if r["extraction_status"] not in ["SUCCESS", "PARTIAL_SUCCESS"])
    salary_count = sum(1 for r in clean_records if r["median_salary_inr"] != "")
    placed_count = sum(1 for r in clean_records if r["placed_count"] != "")
    fee_present = sum(1 for r in clean_records if r["ug_programme_fee_inr"] != "")
    fee_missing = sum(1 for r in clean_records if r["fee_status"] == "NOT_REPORTED_BY_NIRF")
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 85, flush=True)
    print("EXTRACTION SUMMARY & DATA INTEGRITY REPORT", flush=True)
    print("=" * 85, flush=True)
    print(f"Total Colleges Evaluated:            {total_eval}", flush=True)
    print(f"Unique Institute IDs:                {unique_ids}", flush=True)
    print(f"Full Placement Extractions (UG4):    {success_count}", flush=True)
    print(f"Partial Placement Extractions:       {partial_count}", flush=True)
    print(f"Colleges without UG 4-Year Section:  {no_ug4_count}", flush=True)
    print(f"Failed PDF Extractions:              {failed_count}", flush=True)
    print(f"Colleges with Valid Median Salary:   {salary_count}", flush=True)
    print(f"Colleges with Valid Placed Counts:   {placed_count}", flush=True)
    print(f"Colleges with Reported Fees:         {fee_present} (0 expected: NIRF excludes student fees)", flush=True)
    print(f"Colleges with Verified Missing Fee:  {fee_missing}", flush=True)
    print(f"Total Pipeline Runtime:              {elapsed:.2f} seconds", flush=True)
    
    # Check for outliers
    salaries = [r["median_salary_lpa"] for r in clean_records if r["median_salary_lpa"] != ""]
    if salaries:
        print(f"\nPlacement Salary Statistics (LPA):", flush=True)
        print(f"  Min Salary:    {min(salaries):.2f} LPA", flush=True)
        print(f"  Median Salary: {sorted(salaries)[len(salaries)//2]:.2f} LPA", flush=True)
        print(f"  Max Salary:    {max(salaries):.2f} LPA", flush=True)
        print(f"  Average Salary:{sum(salaries)/len(salaries):.2f} LPA", flush=True)

    print("\nSAMPLE EXTRACTED DATA (First 15 colleges):", flush=True)
    print("-" * 115, flush=True)
    print(f"{'Rank':<5} | {'College Name':<34} | {'City':<12} | {'Grad':<6} | {'Placed':<6} | {'Salary (LPA)':<13} | {'Fee':<9} | {'Status'}", flush=True)
    print("-" * 115, flush=True)
    for row in clean_records[:15]:
        fee_str = "MISSING" if row["ug_programme_fee_inr"] == "" else f"Rs {row['ug_programme_fee_inr']}"
        sal_str = f"{row['median_salary_lpa']:.2f} LPA" if row['median_salary_lpa'] != "" else "N/A"
        print(f"{row['nirf_rank']:<5} | {row['college_name'][:34]:<34} | {row['city'][:12]:<12} | "
              f"{str(row['graduated_count']):<6} | {str(row['placed_count']):<6} | "
              f"{sal_str:<13} | {fee_str:<9} | {row['extraction_status']}", flush=True)
    print("-" * 115, flush=True)

    print("\nSAMPLE EXTRACTED DATA (Ranks 86-100):", flush=True)
    print("-" * 115, flush=True)
    print(f"{'Rank':<5} | {'College Name':<34} | {'City':<12} | {'Grad':<6} | {'Placed':<6} | {'Salary (LPA)':<13} | {'Fee':<9} | {'Status'}", flush=True)
    print("-" * 115, flush=True)
    for row in clean_records[-15:]:
        fee_str = "MISSING" if row["ug_programme_fee_inr"] == "" else f"Rs {row['ug_programme_fee_inr']}"
        sal_str = f"{row['median_salary_lpa']:.2f} LPA" if row['median_salary_lpa'] != "" else "N/A"
        print(f"{row['nirf_rank']:<5} | {row['college_name'][:34]:<34} | {row['city'][:12]:<12} | "
              f"{str(row['graduated_count']):<6} | {str(row['placed_count']):<6} | "
              f"{sal_str:<13} | {fee_str:<9} | {row['extraction_status']}", flush=True)
    print("-" * 115, flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NIRF Data Pipeline")
    parser.add_argument("--limit", type=int, default=100, help="Number of colleges to extract (default: 100)")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent download workers (default: 5)")
    args = parser.parse_args()
    run_pipeline(limit=args.limit, max_workers=args.workers)
