import os, json, re, urllib.request, urllib.parse, sys
tok = os.environ['AIRTABLE_TOKEN']
BASE = "applWRIFU0rPBIgTe"; TBL = "Intake Staging"
def fetch():
    recs = []; off = None
    while True:
        u = f"https://api.airtable.com/v0/{BASE}/{urllib.parse.quote(TBL)}?pageSize=100" + (f"&offset={off}" if off else "")
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"})))
        recs += d["records"]; off = d.get("offset")
        if not off: break
    return recs
def norm(s):
    s = (s or "").lower()
    s = re.sub(r'\([^)]*\)', ' ', s)          # drop (nicknames)
    s = re.sub(r'["“”]', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
recs = fetch()
R = []
for r in recs:
    f = r["fields"]
    R.append({
        "id": r["id"], "name": f.get("Name", ""),
        "email": (f.get("Primary Email") or "").strip().lower(),
        "gh": (f.get("GitHub Handle") or "").strip().lower(),
        "src": (f.get("Import Source") or "(none)"),
        "cop": f.get("Community of Practice") or [],
        "status": f.get("Engagement Status") or "",
        "nn": norm(f.get("Name", "")),
    })
# union-find
parent = {r["id"]: r["id"] for r in R}
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    parent[find(a)] = find(b)
by = {}
for r in R:
    for k in [("e", r["email"]), ("g", r["gh"])]:
        if k[1]:
            by.setdefault(k, []).append(r["id"])
for ids in by.values():
    for i in ids[1:]: union(ids[0], i)
def name_match(a, b):
    ta, tb = a["nn"].split(), b["nn"].split()
    if len(ta) < 2 or len(tb) < 2: return False
    fa, la, fb, lb = ta[0], ta[-1], tb[0], tb[-1]
    fok = fa == fb or fa.startswith(fb) or fb.startswith(fa)
    lok = la == lb or la.startswith(lb) or lb.startswith(la)
    return fok and lok
for i in range(len(R)):
    for j in range(i + 1, len(R)):
        if R[i]["src"] != "(none)" and R[j]["src"] != "(none)" and name_match(R[i], R[j]):
            union(R[i]["id"], R[j]["id"])
clusters = {}
for r in R: clusters.setdefault(find(r["id"]), []).append(r)
merges = [c for c in clusters.values() if len(c) > 1]
singles = [c[0] for c in clusters.values() if len(c) == 1 and c[0]["src"] != "(none)"]
def resolve_status(srcs):
    if "Adam roster" in srcs: return "Engaged"
    if "GitHub profile" in srcs or "Liani roster" in srcs: return "Unengaged"
    return "Archived"
def strong(c):  # shared email or gh across the cluster
    es = [x["email"] for x in c if x["email"]]; gs = [x["gh"] for x in c if x["gh"]]
    return (len(es) != len(set(es))) or (len(gs) != len(set(gs))) or (len(set(es)) == 1 and len(es) > 1) or (len(set(gs)) == 1 and len(gs) > 1)
merges.sort(key=lambda c: (-len(c), c[0]["name"].lower()))
out = ["---", "tags:", "  - open-austin", "  - vrm", "  - import", "---",
       "# VRM Dedup Approval Slate", "",
       "Piece-by-piece merge proposals for collapsing Intake Staging into People. Companion to [vrm-import-normalization.md](vrm-import-normalization.md). Base `applWRIFU0rPBIgTe`, Intake Staging `tbldmJXE2WnvSX6xD`, People `tblWu2q7Zmkx4Lsz6`.",
       "",
       "How to use: go through each **M#** below and mark the Decision. On approve, merge the listed staging rows into ONE People record (union fields, accrue all History Flags, use the proposed status, pick one UUID), then delete/flag the merged staging rows. `high` = rows share an email or GitHub handle; `review` = matched on name only, so eyeball it. Singletons at the bottom get promoted 1:1, no merge decision.",
       "", f"Generated 2026-08-11: **{len(merges)} merge clusters**, **{len(singles)} singletons**, from 189 staged rows.", ""]
for n, c in enumerate(merges, 1):
    srcs = sorted({x["src"] for x in c})
    cops = sorted({v for x in c for v in x["cop"]})
    conf = "high" if strong(c) else "review (name-only match)"
    names = sorted({x["name"] for x in c})
    out.append(f"### M{n} — {names[0]}  ({conf})")
    for x in c:
        out.append(f"- [{x['src']}] {x['name']} | {x['email'] or '-'} | gh:{x['gh'] or '-'} | {x['cop']} | {x['status']} | `{x['id']}`")
    out.append(f"- **Proposed Person:** {names[0]}"
               + (f" (also seen as: {', '.join(names[1:])})" if len(names) > 1 else "")
               + f"; CoP {cops or '[]'}; History Flags {srcs}; Status **{resolve_status(srcs)}**.")
    out.append("- Decision: [ ] approve merge  [ ] keep separate  [ ] needs review")
    out.append("")
out.append("## Singletons (promote 1:1, no merge decision)")
for x in sorted(singles, key=lambda x: x["name"].lower()):
    out.append(f"- {x['name']} | [{x['src']}] | {x['email'] or '-'} | gh:{x['gh'] or '-'} | {x['status']}")
open(sys.argv[1], "w").write("\n".join(out))
print(f"{len(merges)} merge clusters, {len(singles)} singletons -> {sys.argv[1]}")
