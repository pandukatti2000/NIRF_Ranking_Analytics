"""
Comprehensive research and data extraction script for all 100 NIRF colleges.
Compiles official fee figures, source URLs, source types, and breakdowns.
"""

import csv
import json

# Load colleges_clean
with open('colleges_clean.csv', encoding='utf-8') as f:
    colleges = list(csv.DictReader(f))

print(f"Loaded {len(colleges)} colleges.")

# Let's inspect the remaining institutions to ensure every single one has an exact verified fee schedule
# Group remaining institutes:
# - State & Central Universities: Jadavpur, Anna, Jamia, DTU, AMU, ICT Mumbai, NSUT, MMMUT, Panjab Univ, JNTUH, AU College
# - IIITs: IIIT Hyderabad, IIIT Delhi, ABV-IIITM Gwalior
# - Private / Deemed Universities: BITS, SRM, VIT, Thapar, Amrita, SOA, KL Univ, KIIT, Amity, SASTRA, UPES, Symbiosis, SSN, LPU, BIT Mesra, Graphic Era, Manipal, IIST, Sathyabama, PSG Tech, Banasthali, MS Ramaiah, Christ, RGIPT, SLIET, Vignan, Jain, Vel Tech, Chitkara, SR Univ, CV Raman, PDEU, Sri Krishna
