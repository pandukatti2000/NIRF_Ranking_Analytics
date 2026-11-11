"""
Scale-Up Fee Generation and Value-for-Money Pipeline
Compiles official B.Tech fee data for all 100 NIRF colleges, validates schemas,
merges with placement dataset, and generates final analysis artifacts.
"""

import csv
import json
import os
import re

CLEAN_COLLEGES_CSV = "colleges_clean.csv"
FEE_RAW_CSV = "college_fees_raw.csv"
FEE_CLEAN_CSV = "college_fees_clean.csv"
FEE_ISSUES_CSV = "fee_extraction_issues.csv"
COLLEGES_FINAL_CSV = "colleges_final.csv"
FEE_SOURCES_MD = "fee_sources.md"

# Load the existing colleges_clean.csv dataset (100 rows)
with open(CLEAN_COLLEGES_CSV, "r", encoding="utf-8") as f:
    colleges = list(csv.DictReader(f))

assert len(colleges) == 100, f"Expected 100 colleges, got {len(colleges)}"

print(f"Loaded {len(colleges)} colleges from {CLEAN_COLLEGES_CSV}")
