import csv

with open('colleges_clean.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total colleges: {len(rows)}")

iits = []
nits = []
iiits = []
other_govt = []
private_deemed = []

for r in rows:
    name = r['college_name']
    c_id = r['institute_id']
    rank = int(r['nirf_rank'])
    
    if 'Indian Institute of Technology' in name or 'IIT' in name:
        iits.append((rank, c_id, name))
    elif 'National Institute of Technology' in name or 'NIT' in name or 'Malaviya' in name or 'Motilal Nehru' in name or 'Visvesvaraya' in name or 'Maulana Azad' in name or 'Dr. B R Ambedkar' in name:
        nits.append((rank, c_id, name))
    elif 'Indian Institute of Information Technology' in name or 'IIIT' in name:
        iiits.append((rank, c_id, name))
    elif any(term in name for term in ['University', 'College of Engineering', 'Institute of Chemical Technology', 'Jadavpur', 'Delhi Technological', 'Netaji Subhas', 'Anna University', 'Aligarh', 'Jamia', 'Punjab Engineering']):
        other_govt.append((rank, c_id, name))
    else:
        private_deemed.append((rank, c_id, name))

print(f"IITs ({len(iits)}): {[x[0] for x in iits]}")
print(f"NITs/CFTIs ({len(nits)}): {[x[0] for x in nits]}")
print(f"IIITs ({len(iiits)}): {[x[0] for x in iiits]}")
print(f"Other Govt / Univ ({len(other_govt)}): {[x[0] for x in other_govt]}")
print(f"Private / Deemed ({len(private_deemed)}): {[x[0] for x in private_deemed]}")
