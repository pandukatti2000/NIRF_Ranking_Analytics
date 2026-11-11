"""
Deep Value-for-Money Analytics for NIRF 2025 Engineering Colleges.
Computes:
1. Overall summary statistics (fees, salaries, recovery years, placement %).
2. Rank Band analysis (Bands 1-25, 26-50, 51-75, 76-100).
3. State-level comparative analysis.
4. Top 10 Best Value colleges (Lowest recovery years / Highest ROI).
5. Top 10 Worst Value colleges (Highest recovery years / Lowest relative return).
6. Scatter data for interactive dashboard.
"""

import csv
import json
from collections import defaultdict

with open('colleges_final.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Filter eligible colleges (with both valid fee and salary)
eligible = [r for r in rows if r['fee_salary_ratio'] != '']
print(f"Total rows: {len(rows)}, Eligible for VFM analysis: {len(eligible)}")

# Assign Rank Bands
for r in eligible:
    rank = int(r['nirf_rank'])
    if rank <= 25:
        r['rank_band'] = 'Band 1 (Ranks 1-25)'
    elif rank <= 50:
        r['rank_band'] = 'Band 2 (Ranks 26-50)'
    elif rank <= 75:
        r['rank_band'] = 'Band 3 (Ranks 51-75)'
    else:
        r['rank_band'] = 'Band 4 (Ranks 76-100)'

# 1. Overall Metrics
fees = [float(r['total_4yr_academic_fees_lpa']) for r in eligible]
salaries = [float(r['median_salary_lpa']) for r in eligible]
ratios = [float(r['fee_salary_ratio']) for r in eligible]
placement_rates = [float(r['placement_percentage']) for r in eligible if r['placement_percentage'] != '']

print("\n" + "="*80)
print("OVERALL COHORT SUMMARY (97 Verified Institutions)")
print("="*80)
print(f"Average 4-Year Academic Fees:     Rs {sum(fees)/len(fees):.2f} Lakhs (Min: Rs {min(fees):.2f}L, Max: Rs {max(fees):.2f}L)")
print(f"Median 4-Year Academic Fees:      Rs {sorted(fees)[len(fees)//2]:.2f} Lakhs")
print(f"Average Annual Median Salary:     Rs {sum(salaries)/len(salaries):.2f} LPA (Min: Rs {min(salaries):.2f}L, Max: Rs {max(salaries):.2f}L)")
print(f"Median of Annual Median Salaries: Rs {sorted(salaries)[len(salaries)//2]:.2f} LPA")
print(f"Average Fee Recovery Period:      {sum(ratios)/len(ratios):.2f} Years of Salary (Min: {min(ratios):.3f} yrs, Max: {max(ratios):.3f} yrs)")
print(f"Median Fee Recovery Period:       {sorted(ratios)[len(ratios)//2]:.2f} Years of Salary")
print(f"Average Placement Percentage:     {sum(placement_rates)/len(placement_rates):.2f}% (Min: {min(placement_rates):.1f}%, Max: {max(placement_rates):.1f}%)")

# 2. Rank Band Analysis
bands = ['Band 1 (Ranks 1-25)', 'Band 2 (Ranks 26-50)', 'Band 3 (Ranks 51-75)', 'Band 4 (Ranks 76-100)']
band_stats = {}

print("\n" + "="*80)
print("ANALYSIS BY NIRF RANK BAND")
print("="*80)
for b in bands:
    b_rows = [r for r in eligible if r['rank_band'] == b]
    b_fees = [float(r['total_4yr_academic_fees_lpa']) for r in b_rows]
    b_sals = [float(r['median_salary_lpa']) for r in b_rows]
    b_rats = [float(r['fee_salary_ratio']) for r in b_rows]
    b_place = [float(r['placement_percentage']) for r in b_rows if r['placement_percentage'] != '']
    
    band_stats[b] = {
        'count': len(b_rows),
        'avg_fee_lpa': round(sum(b_fees)/len(b_fees), 2),
        'median_fee_lpa': round(sorted(b_fees)[len(b_fees)//2], 2),
        'avg_salary_lpa': round(sum(b_sals)/len(b_sals), 2),
        'median_salary_lpa': round(sorted(b_sals)[len(b_sals)//2], 2),
        'avg_ratio': round(sum(b_rats)/len(b_rats), 3),
        'median_ratio': round(sorted(b_rats)[len(b_rats)//2], 3),
        'avg_placement_pct': round(sum(b_place)/len(b_place), 2)
    }
    
    print(f"\n--- {b} ({len(b_rows)} Colleges) ---")
    print(f"  Avg 4-Year Fees:        Rs {band_stats[b]['avg_fee_lpa']} Lakhs")
    print(f"  Avg Median Salary:      Rs {band_stats[b]['avg_salary_lpa']} LPA")
    print(f"  Avg Fee Recovery Ratio: {band_stats[b]['avg_ratio']} Years of Salary")
    print(f"  Avg Placement Rate:     {band_stats[b]['avg_placement_pct']}%")

# 3. State Analysis
state_groups = defaultdict(list)
for r in eligible:
    state_groups[r['state']].append(r)

state_stats = []
for state, s_rows in state_groups.items():
    if len(s_rows) >= 2: # States with at least 2 ranked colleges
        s_fees = [float(r['total_4yr_academic_fees_lpa']) for r in s_rows]
        s_sals = [float(r['median_salary_lpa']) for r in s_rows]
        s_rats = [float(r['fee_salary_ratio']) for r in s_rows]
        s_place = [float(r['placement_percentage']) for r in s_rows if r['placement_percentage'] != '']
        state_stats.append({
            'state': state,
            'college_count': len(s_rows),
            'avg_fee_lpa': round(sum(s_fees)/len(s_fees), 2),
            'avg_salary_lpa': round(sum(s_sals)/len(s_sals), 2),
            'avg_recovery_years': round(sum(s_rats)/len(s_rats), 3),
            'avg_placement_pct': round(sum(s_place)/len(s_place), 2)
        })

state_stats.sort(key=lambda x: x['avg_recovery_years'])

print("\n" + "="*80)
print("STATE-LEVEL VALUE COMPARISON (States with >= 2 ranked colleges)")
print("="*80)
for s in state_stats:
    print(f"{s['state']:<20} | Colleges: {s['college_count']:>2} | Avg Fees: Rs {s['avg_fee_lpa']:>5.2f}L | Avg Salary: {s['avg_salary_lpa']:>5.2f} LPA | Recovery: {s['avg_recovery_years']:>5.3f} yrs | Placement: {s['avg_placement_pct']}%")

# 4. Top 10 Best Value Colleges
sorted_best = sorted(eligible, key=lambda x: float(x['fee_salary_ratio']))
print("\n" + "="*80)
print("TOP 10 BEST VALUE ENGINEERING COLLEGES (Lowest Fee Recovery Years)")
print("="*80)
for idx, r in enumerate(sorted_best[:10], 1):
    print(f"{idx:>2}. Rank {r['nirf_rank']:>3} | {r['college_name'][:38]:<38} | {r['state'][:12]:<12} | Fee: Rs {float(r['total_4yr_academic_fees_lpa']):>5.2f}L | Salary: {float(r['median_salary_lpa']):>5.2f} LPA | Recovery: {float(r['fee_salary_ratio']):>5.3f} yrs | Placement: {r['placement_percentage']}%")

# 5. Top 10 Worst Value Colleges
sorted_worst = sorted(eligible, key=lambda x: float(x['fee_salary_ratio']), reverse=True)
print("\n" + "="*80)
print("TOP 10 WORST VALUE ENGINEERING COLLEGES (Highest Fee Recovery Years)")
print("="*80)
for idx, r in enumerate(sorted_worst[:10], 1):
    print(f"{idx:>2}. Rank {r['nirf_rank']:>3} | {r['college_name'][:38]:<38} | {r['state'][:12]:<12} | Fee: Rs {float(r['total_4yr_academic_fees_lpa']):>5.2f}L | Salary: {float(r['median_salary_lpa']):>5.2f} LPA | Recovery: {float(r['fee_salary_ratio']):>5.3f} yrs | Placement: {r['placement_percentage']}%")

# Save complete analytics data to JSON for dashboard rendering
analytics_export = {
    'summary': {
        'total_institutions': 100,
        'eligible_vfm_institutions': len(eligible),
        'pg_only_institutions': len(rows) - len(eligible),
        'avg_fees_lpa': round(sum(fees)/len(fees), 2),
        'median_fees_lpa': round(sorted(fees)[len(fees)//2], 2),
        'avg_salary_lpa': round(sum(salaries)/len(salaries), 2),
        'median_salary_lpa': round(sorted(salaries)[len(salaries)//2], 2),
        'avg_recovery_years': round(sum(ratios)/len(ratios), 3),
        'median_recovery_years': round(sorted(ratios)[len(ratios)//2], 3),
        'avg_placement_pct': round(sum(placement_rates)/len(placement_rates), 2)
    },
    'rank_bands': band_stats,
    'states': state_stats,
    'top_10_best': [{
        'rank': int(r['nirf_rank']),
        'name': r['college_name'],
        'state': r['state'],
        'fees_lpa': float(r['total_4yr_academic_fees_lpa']),
        'salary_lpa': float(r['median_salary_lpa']),
        'recovery_years': float(r['fee_salary_ratio']),
        'placement_pct': float(r['placement_percentage'])
    } for r in sorted_best[:10]],
    'top_10_worst': [{
        'rank': int(r['nirf_rank']),
        'name': r['college_name'],
        'state': r['state'],
        'fees_lpa': float(r['total_4yr_academic_fees_lpa']),
        'salary_lpa': float(r['median_salary_lpa']),
        'recovery_years': float(r['fee_salary_ratio']),
        'placement_pct': float(r['placement_percentage'])
    } for r in sorted_worst[:10]],
    'all_colleges': [{
        'id': r['institute_id'],
        'rank': int(r['nirf_rank']),
        'name': r['college_name'],
        'city': r['city'],
        'state': r['state'],
        'rank_band': r['rank_band'],
        'fees_lpa': float(r['total_4yr_academic_fees_lpa']),
        'salary_lpa': float(r['median_salary_lpa']),
        'recovery_years': float(r['fee_salary_ratio']),
        'placement_pct': float(r['placement_percentage']) if r['placement_percentage'] != '' else None,
        'placed': int(r['placed_count']) if r['placed_count'] else None,
        'graduated': int(r['graduated_count']) if r['graduated_count'] else None,
        'source_type': r['fee_source_type'],
        'source_url': r['fee_source_url']
    } for r in eligible]
}

with open('analytics_summary.json', 'w', encoding='utf-8') as f:
    json.dump(analytics_export, f, indent=2)

print("\n[OUTPUT] Saved complete analytics payload to analytics_summary.json")
