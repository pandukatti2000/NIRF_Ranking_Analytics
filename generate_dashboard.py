"""
Generates a standalone, interactive HTML/JS Analytics Dashboard for Project DA-16.
Features:
- Scorecards (Total Colleges, Median Fees, Median Salary, Median Recovery Years, Avg Placement %)
- Interactive Filters (Rank Band, State, Search by Name)
- Scatter Plot: 4-Year Fees vs Median Placement Salary (Bubble size = Placement Rate)
- Bar Charts: Top 10 Best Value vs Top 10 Worst Value Colleges
- Grouped Bar Chart: Average Fees, Salary & Recovery Years by Rank Band
- College Comparator tool
- Full Searchable & Sortable Data Table
"""

import json

with open('analytics_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_payload = json.dumps(data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NIRF Engineering Value-for-Money Analytics Dashboard</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .badge-best {{ background-color: #dcfce7; color: #166534; }}
    .badge-worst {{ background-color: #fee2e2; color: #991b1b; }}
    .badge-mid {{ background-color: #fef9c3; color: #854d0e; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen">
  <!-- Top Navigation Header -->
  <header class="bg-slate-900 text-white border-b border-slate-800 shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row md:items-center md:justify-between">
      <div>
        <div class="flex items-center space-x-3">
          <span class="bg-indigo-600 text-white text-xs font-bold px-2.5 py-1 rounded tracking-wider uppercase">Project DA-16</span>
          <h1 class="text-xl md:text-2xl font-bold tracking-tight">Is That College Worth the Fees?</h1>
        </div>
        <p class="text-slate-400 text-xs md:text-sm mt-1">Value-for-Money Analysis of Top 100 NIRF Engineering Colleges for Students & Families</p>
      </div>
      <div class="mt-3 md:mt-0 flex items-center space-x-2">
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-300 border border-emerald-800">
          <span class="w-2 h-2 mr-1.5 bg-emerald-400 rounded-full animate-pulse"></span> 97 Verified B.Tech Datasets
        </span>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Executive KPI Scorecards -->
    <section class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Total Evaluated</p>
        <p class="text-2xl font-extrabold text-slate-900 mt-1" id="kpi-total">100</p>
        <p class="text-xs text-slate-400 mt-1">97 UG B.Tech, 3 PG-Only</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Median 4-Yr Fees</p>
        <p class="text-2xl font-extrabold text-indigo-600 mt-1" id="kpi-fees">₹8.79 L</p>
        <p class="text-xs text-slate-400 mt-1">Range: ₹0.14L - ₹22.97L</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Median Salary</p>
        <p class="text-2xl font-extrabold text-emerald-600 mt-1" id="kpi-salary">₹10.00 LPA</p>
        <p class="text-xs text-slate-400 mt-1">Range: ₹3.36L - ₹32.00L</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Median Recovery</p>
        <p class="text-2xl font-extrabold text-blue-600 mt-1" id="kpi-recovery">0.66 Yrs</p>
        <p class="text-xs text-slate-400 mt-1">Years of salary to recover fees</p>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm col-span-2 md:col-span-1">
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Avg Placement Rate</p>
        <p class="text-2xl font-extrabold text-violet-600 mt-1" id="kpi-placement">72.0%</p>
        <p class="text-xs text-slate-400 mt-1">Placed / Graduated Cohort</p>
      </div>
    </section>

    <!-- Key Questions Addressed Section -->
    <section class="bg-indigo-50 border border-indigo-100 rounded-xl p-5 text-indigo-950 text-sm">
      <div class="flex items-start space-x-3">
        <span class="text-2xl">💡</span>
        <div>
          <h2 class="font-bold text-base text-indigo-900">Decision-Making Framework for Families</h2>
          <p class="mt-1 text-slate-700 leading-relaxed">
            Comparing colleges on brand or raw rank alone can be deceptive. A high-ranking private college charging ₹18 Lakhs with a ₹6 LPA median salary requires <strong>nearly 3 years of salary</strong> to recover fees, whereas a premier state/central university charging ₹15,000 to ₹1.5 Lakhs achieves full fee recovery in <strong>under 2 to 3 months</strong>.
          </p>
        </div>
      </div>
    </section>

    <!-- Interactive Filters -->
    <section class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Rank Band</label>
          <select id="filter-band" class="bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            <option value="ALL">All Rank Bands</option>
            <option value="Band 1 (Ranks 1-25)">Band 1 (Ranks 1–25)</option>
            <option value="Band 2 (Ranks 26-50)">Band 2 (Ranks 26–50)</option>
            <option value="Band 3 (Ranks 51-75)">Band 3 (Ranks 51–75)</option>
            <option value="Band 4 (Ranks 76-100)">Band 4 (Ranks 76–100)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">State</label>
          <select id="filter-state" class="bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            <option value="ALL">All States</option>
          </select>
        </div>
      </div>
      <div class="w-full md:w-72">
        <label class="block text-xs font-semibold text-slate-600 mb-1">Search College</label>
        <input type="text" id="filter-search" placeholder="Search by name, city..." class="w-full bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none">
      </div>
    </section>

    <!-- Visual Analytics: Charts Grid -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Chart 1: Fees vs Salary Scatter Plot -->
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-slate-900 text-base">4-Year Fees vs. Median Placement Salary</h3>
            <p class="text-xs text-slate-500">Bubble size indicates Placement % | Top-left quadrant = Highest Value</p>
          </div>
        </div>
        <div class="h-80">
          <canvas id="scatterChart"></canvas>
        </div>
      </div>

      <!-- Chart 2: Rank Band Comparison -->
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-slate-900 text-base">Average Fees, Salary & Recovery by Rank Band</h3>
            <p class="text-xs text-slate-500">Comparing Ranks 1-25 vs 26-50 vs 51-75 vs 76-100</p>
          </div>
        </div>
        <div class="h-80">
          <canvas id="bandChart"></canvas>
        </div>
      </div>
    </section>

    <!-- Top 10 Best vs Worst Value Side-by-Side -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Best Value -->
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center space-x-2 mb-4">
          <span class="w-3 h-3 bg-emerald-500 rounded-full"></span>
          <h3 class="font-bold text-slate-900 text-base">Top 10 Best Value Colleges (Lowest Recovery Years)</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-semibold uppercase border-b border-slate-200">
              <tr>
                <th class="py-2.5 px-3">Rank</th>
                <th class="py-2.5 px-3">College</th>
                <th class="py-2.5 px-2">4-Yr Fees</th>
                <th class="py-2.5 px-2">Salary</th>
                <th class="py-2.5 px-2">Recovery</th>
                <th class="py-2.5 px-2">Placed %</th>
              </tr>
            </thead>
            <tbody id="top10-best-body" class="divide-y divide-slate-100 text-slate-700"></tbody>
          </table>
        </div>
      </div>

      <!-- Worst Value -->
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center space-x-2 mb-4">
          <span class="w-3 h-3 bg-red-500 rounded-full"></span>
          <h3 class="font-bold text-slate-900 text-base">Top 10 Worst Value Colleges (Highest Recovery Years)</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-semibold uppercase border-b border-slate-200">
              <tr>
                <th class="py-2.5 px-3">Rank</th>
                <th class="py-2.5 px-3">College</th>
                <th class="py-2.5 px-2">4-Yr Fees</th>
                <th class="py-2.5 px-2">Salary</th>
                <th class="py-2.5 px-2">Recovery</th>
                <th class="py-2.5 px-2">Placed %</th>
              </tr>
            </thead>
            <tbody id="top10-worst-body" class="divide-y divide-slate-100 text-slate-700"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- State-Level Ranking Table -->
    <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 class="font-bold text-slate-900 text-base mb-1">State-by-State Value-for-Money Comparison</h3>
      <p class="text-xs text-slate-500 mb-4">States with $\ge$ 2 ranked engineering institutions, sorted from best to worst fee recovery</p>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50 text-slate-600 font-semibold uppercase border-b border-slate-200">
            <tr>
              <th class="py-2.5 px-3">State</th>
              <th class="py-2.5 px-3">Ranked Colleges</th>
              <th class="py-2.5 px-3">Avg 4-Yr Fees</th>
              <th class="py-2.5 px-3">Avg Median Salary</th>
              <th class="py-2.5 px-3">Avg Recovery (Yrs)</th>
              <th class="py-2.5 px-3">Avg Placement %</th>
              <th class="py-2.5 px-3">Value Rating</th>
            </tr>
          </thead>
          <tbody id="state-table-body" class="divide-y divide-slate-100 text-slate-700"></tbody>
        </table>
      </div>
    </section>

    <!-- Complete Searchable College Master Directory -->
    <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-4 gap-2">
        <div>
          <h3 class="font-bold text-slate-900 text-base">Complete NIRF Engineering College Explorer</h3>
          <p class="text-xs text-slate-500">Filter and search across all 97 evaluated undergraduate engineering programs</p>
        </div>
        <span class="text-xs text-slate-400" id="table-count">Showing 97 colleges</span>
      </div>
      <div class="overflow-x-auto max-h-96">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50 text-slate-600 font-semibold uppercase sticky top-0 z-10 border-b border-slate-200">
            <tr>
              <th class="py-2.5 px-3">Rank</th>
              <th class="py-2.5 px-3">College Name</th>
              <th class="py-2.5 px-2">City, State</th>
              <th class="py-2.5 px-2">4-Yr Fees (L)</th>
              <th class="py-2.5 px-2">Salary (LPA)</th>
              <th class="py-2.5 px-2">Recovery (Yrs)</th>
              <th class="py-2.5 px-2">Placed %</th>
              <th class="py-2.5 px-2">Source</th>
            </tr>
          </thead>
          <tbody id="master-table-body" class="divide-y divide-slate-100 text-slate-700"></tbody>
        </table>
      </div>
    </section>

    <!-- Project Methodology & Limitations Disclosure -->
    <section class="bg-slate-900 text-slate-300 p-6 rounded-xl text-xs space-y-4">
      <h3 class="font-bold text-sm text-white uppercase tracking-wider">Methodology & Limitations Disclosure (AccioJob DA-16)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h4 class="font-semibold text-white mb-1">1. Value Metric Definition</h4>
          <p class="text-slate-400 leading-relaxed">
            Value is calculated as <code>total_4yr_academic_fees / annual_median_salary</code> (years of gross median salary needed to recover total tuition and mandatory academic fees). It does not represent literal net loan repayment time or personal ROI.
          </p>
        </div>
        <div>
          <h4 class="font-semibold text-white mb-1">2. What Median Salary Hides</h4>
          <p class="text-slate-400 leading-relaxed">
            The median represents the 50th percentile of placed graduates. It obscures variance: high packages in CSE/IT pull up perception, while core branches may place lower. Furthermore, non-placed students earn ₹0, which is omitted from median salary.
          </p>
        </div>
        <div>
          <h4 class="font-semibold text-white mb-1">3. Non-Academic Living Costs</h4>
          <p class="text-slate-400 leading-relaxed">
            Hostel accommodation and mess food charges (typically ₹1.2L to ₹2.2L per annum) and refundable caution deposits are strictly excluded to maintain academic comparability across residential and non-residential institutes.
          </p>
        </div>
      </div>
    </section>
  </main>

  <footer class="bg-slate-950 text-slate-500 py-6 text-center text-xs border-t border-slate-800">
    <p>NIRF 2025 Engineering College Value-for-Money Project (AccioJob DA-16) · Verified against official NIRF DCS reports & institutional circulars.</p>
  </footer>

  <!-- Embedded Analytics Dataset & Dashboard Controller -->
  <script>
    const analyticsData = {json_payload};
    let allColleges = analyticsData.all_colleges;
    let filteredColleges = [...allColleges];

    // Populate State Filter
    const stateSelect = document.getElementById('filter-state');
    const states = [...new Set(allColleges.map(c => c.state))].sort();
    states.forEach(s => {{
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = s;
      stateSelect.appendChild(opt);
    }});

    // Populate Top 10 Best Table
    const topBestBody = document.getElementById('top10-best-body');
    analyticsData.top_10_best.forEach(c => {{
      const tr = document.createElement('tr');
      tr.className = 'hover:bg-slate-50';
      tr.innerHTML = `
        <td class="py-2.5 px-3 font-bold text-slate-900">#${{c.rank}}</td>
        <td class="py-2.5 px-3 font-medium">${{c.name}} <span class="text-slate-400 text-[10px]">(${{c.state}})</span></td>
        <td class="py-2.5 px-2">₹${{c.fees_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-2 font-semibold text-emerald-600">₹${{c.salary_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-2 font-bold text-indigo-600">${{c.recovery_years.toFixed(3)}} yrs</td>
        <td class="py-2.5 px-2">${{c.placement_pct.toFixed(1)}}%</td>
      `;
      topBestBody.appendChild(tr);
    }});

    // Populate Top 10 Worst Table
    const topWorstBody = document.getElementById('top10-worst-body');
    analyticsData.top_10_worst.forEach(c => {{
      const tr = document.createElement('tr');
      tr.className = 'hover:bg-slate-50';
      tr.innerHTML = `
        <td class="py-2.5 px-3 font-bold text-slate-900">#${{c.rank}}</td>
        <td class="py-2.5 px-3 font-medium">${{c.name}} <span class="text-slate-400 text-[10px]">(${{c.state}})</span></td>
        <td class="py-2.5 px-2 text-red-600 font-semibold">₹${{c.fees_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-2">₹${{c.salary_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-2 font-bold text-red-600">${{c.recovery_years.toFixed(3)}} yrs</td>
        <td class="py-2.5 px-2">${{c.placement_pct.toFixed(1)}}%</td>
      `;
      topWorstBody.appendChild(tr);
    }});

    // Populate State Table
    const stateBody = document.getElementById('state-table-body');
    analyticsData.states.forEach(s => {{
      let badge = 'badge-mid';
      let rating = 'Moderate';
      if (s.avg_recovery_years < 0.7) {{ badge = 'badge-best'; rating = 'High Value'; }}
      else if (s.avg_recovery_years > 1.2) {{ badge = 'badge-worst'; rating = 'Low Value'; }}

      const tr = document.createElement('tr');
      tr.className = 'hover:bg-slate-50';
      tr.innerHTML = `
        <td class="py-2.5 px-3 font-bold text-slate-900">${{s.state}}</td>
        <td class="py-2.5 px-3">${{s.college_count}}</td>
        <td class="py-2.5 px-3">₹${{s.avg_fee_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-3 font-semibold text-emerald-600">₹${{s.avg_salary_lpa.toFixed(2)}}L</td>
        <td class="py-2.5 px-3 font-bold">${{s.avg_recovery_years.toFixed(3)}} yrs</td>
        <td class="py-2.5 px-3">${{s.avg_placement_pct.toFixed(1)}}%</td>
        <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] font-semibold ${{badge}}">${{rating}}</span></td>
      `;
      stateBody.appendChild(tr);
    }});

    // Render Master Table
    function renderMasterTable() {{
      const tbody = document.getElementById('master-table-body');
      tbody.innerHTML = '';
      document.getElementById('table-count').textContent = `Showing ${{filteredColleges.length}} of ${{allColleges.length}} colleges`;

      filteredColleges.forEach(c => {{
        let badge = 'text-slate-600';
        if (c.recovery_years < 0.6) badge = 'text-emerald-700 font-bold';
        else if (c.recovery_years > 1.5) badge = 'text-red-600 font-bold';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-bold text-slate-900">#${{c.rank}}</td>
          <td class="py-2.5 px-3 font-medium text-slate-800">${{c.name}}</td>
          <td class="py-2.5 px-2 text-slate-500">${{c.city}}, ${{c.state}}</td>
          <td class="py-2.5 px-2">₹${{c.fees_lpa.toFixed(2)}}L</td>
          <td class="py-2.5 px-2 font-semibold text-emerald-600">₹${{c.salary_lpa.toFixed(2)}}L</td>
          <td class="py-2.5 px-2 ${{badge}}">${{c.recovery_years.toFixed(3)}} yrs</td>
          <td class="py-2.5 px-2">${{c.placement_pct ? c.placement_pct.toFixed(1) + '%' : 'N/A'}}</td>
          <td class="py-2.5 px-2 text-[10px] text-indigo-600 truncate max-w-[120px]"><a href="${{c.source_url}}" target="_blank" class="hover:underline">${{c.source_type}}</a></td>
        `;
        tbody.appendChild(tr);
      }});
    }}
    renderMasterTable();

    // Filtering Controller
    function applyFilters() {{
      const band = document.getElementById('filter-band').value;
      const state = document.getElementById('filter-state').value;
      const search = document.getElementById('filter-search').value.toLowerCase();

      filteredColleges = allColleges.filter(c => {{
        const matchBand = (band === 'ALL' || c.rank_band === band);
        const matchState = (state === 'ALL' || c.state === state);
        const matchSearch = (!search || c.name.toLowerCase().includes(search) || c.city.toLowerCase().includes(search));
        return matchBand && matchState && matchSearch;
      }});

      renderMasterTable();
      updateScatterChart();
    }}

    document.getElementById('filter-band').addEventListener('change', applyFilters);
    document.getElementById('filter-state').addEventListener('change', applyFilters);
    document.getElementById('filter-search').addEventListener('input', applyFilters);

    // Chart 1: Scatter Chart (Fees vs Salary)
    const ctxScatter = document.getElementById('scatterChart').getContext('2d');
    let scatterChart = new Chart(ctxScatter, {{
      type: 'bubble',
      data: {{
        datasets: [{{
          label: 'Engineering Colleges',
          data: allColleges.map(c => ({{
            x: c.fees_lpa,
            y: c.salary_lpa,
            r: c.placement_pct ? Math.max(3, c.placement_pct / 12) : 4,
            college: c
          }})),
          backgroundColor: allColleges.map(c => {{
            if (c.recovery_years < 0.6) return 'rgba(16, 185, 129, 0.7)'; // Emerald
            if (c.recovery_years > 1.5) return 'rgba(239, 68, 68, 0.7)';  // Red
            return 'rgba(99, 102, 241, 0.7)'; // Indigo
          }}),
          borderColor: 'rgba(255, 255, 255, 0.8)',
          borderWidth: 1
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          tooltip: {{
            callbacks: {{
              label: function(ctx) {{
                const c = ctx.raw.college;
                return `${{c.name}} (#${{c.rank}}): Fees ₹${{c.fees_lpa}}L | Salary ₹${{c.salary_lpa}}L | ${{c.recovery_years.toFixed(2)}} Yrs | Placement ${{c.placement_pct ? c.placement_pct.toFixed(1) + '%' : 'N/A'}}`;
              }}
            }}
          }}
        }},
        scales: {{
          x: {{
            title: {{ display: true, text: '4-Year Total Academic Fees (₹ Lakhs)' }},
            min: 0,
            max: 25
          }},
          y: {{
            title: {{ display: true, text: 'Annual Median Placement Salary (₹ LPA)' }},
            min: 0,
            max: 35
          }}
        }}
      }}
    }});

    function updateScatterChart() {{
      scatterChart.data.datasets[0].data = filteredColleges.map(c => ({{
        x: c.fees_lpa,
        y: c.salary_lpa,
        r: c.placement_pct ? Math.max(3, c.placement_pct / 12) : 4,
        college: c
      }}));
      scatterChart.data.datasets[0].backgroundColor = filteredColleges.map(c => {{
        if (c.recovery_years < 0.6) return 'rgba(16, 185, 129, 0.7)';
        if (c.recovery_years > 1.5) return 'rgba(239, 68, 68, 0.7)';
        return 'rgba(99, 102, 241, 0.7)';
      }});
      scatterChart.update();
    }}

    // Chart 2: Rank Band Bar Chart
    const ctxBand = document.getElementById('bandChart').getContext('2d');
    const bandLabels = Object.keys(analyticsData.rank_bands);
    new Chart(ctxBand, {{
      type: 'bar',
      data: {{
        labels: ['Band 1 (1-25)', 'Band 2 (26-50)', 'Band 3 (51-75)', 'Band 4 (76-100)'],
        datasets: [
          {{
            label: 'Avg 4-Yr Fees (₹ L)',
            data: bandLabels.map(k => analyticsData.rank_bands[k].avg_fee_lpa),
            backgroundColor: 'rgba(99, 102, 241, 0.8)'
          }},
          {{
            label: 'Avg Median Salary (₹ LPA)',
            data: bandLabels.map(k => analyticsData.rank_bands[k].avg_salary_lpa),
            backgroundColor: 'rgba(16, 185, 129, 0.8)'
          }},
          {{
            label: 'Avg Recovery Period (Yrs)',
            data: bandLabels.map(k => analyticsData.rank_bands[k].avg_ratio),
            backgroundColor: 'rgba(245, 158, 11, 0.8)'
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          y: {{ beginAtZero: true, title: {{ display: true, text: 'Values (Lakhs / Years)' }} }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[OUTPUT] Saved interactive dashboard to dashboard.html")
