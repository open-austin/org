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
        "id": r["id"], "name": f.get("Name", ""), "f": f,
        "email": (f.get("Primary Email") or "").strip().lower(),
        "gh": (f.get("GitHub Handle") or "").strip().lower(),
        "src": (f.get("Import Source") or "(none)"),
        "cop": f.get("Community of Practice") or [],
        "status": f.get("Engagement Status") or "",
        "notes": f.get("Notes") or "",
        "nn": norm(f.get("Name", "")),
    })

# ---- value helpers ----
def sval(v):
    if isinstance(v, list): return ", ".join(str(x) for x in v)
    return str(v).strip()
def team_hint(notes):
    h = []
    m = re.search(r'Team \(2024 roster\):\s*(.+)', notes)
    if m: h.append("roster-team=" + m.group(1).strip())
    m = re.search(r'Most recent Slack channel:\s*(.+)', notes)
    if m: h.append("slack=" + m.group(1).strip())
    return (" | " + ", ".join(h)) if h else ""
def roster_team(notes):
    m = re.search(r'Team \(2024 roster\):\s*(.+)', notes)
    return m.group(1).strip() if m else ""
def emails_union(c):
    seen = []
    for x in c:
        f = x["f"]
        cands = [f.get("Primary Email") or ""]
        alt = f.get("Alternate Emails")
        if isinstance(alt, str): cands += alt.split()
        for e in cands:
            e = e.strip()
            if e and e.lower() not in [s.lower() for s in seen]:
                seen.append(e)
    return seen
def variants(c, key):
    """value -> sorted list of sources that carried it (non-empty only)."""
    out = {}
    for x in c:
        v = x["f"].get(key)
        if v in (None, "", []): continue
        s = sval(v)
        if not s: continue
        out.setdefault(s, set()).add(x["src"])
    return {k: sorted(v) for k, v in out.items()}
def render_variants(vv):
    if len(vv) == 1:
        return next(iter(vv))
    return "; ".join(f"{v} [{'/'.join(srcs)}]" for v, srcs in vv.items())

# fields with dedicated handling; everything else populated is rendered generically so nothing is dropped
SPECIAL = {"Name", "Primary Email", "Alternate Emails", "GitHub Handle", "Community of Practice",
           "Notes", "UUID", "Import Source", "History Flags", "Engagement Status", "Disengagement Type",
           "Ready to Promote", "Promoted Person", "Product Teams", "Communities of Practice",
           "Standing Teams", "Roles", "Organization"}
PREF = ["Legal Name", "Pronouns", "Phone", "Other Skills", "Wants to Learn", "Wants to learn",
        "Interests", "Skills", "Languages", "Availability", "Effort (hours)", "Location",
        "Willingness to expand roles", "Last Slack Activity", "Last GitHub Activity",
        "Repos Contributed To", "Date First Seen"]

# ---- clustering (union-find over shared email / gh / fuzzy name) ----
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

# ---- merged-union preview for one cluster ----
def proposed_block(c):
    names = sorted({x["name"] for x in c})
    srcs = sorted({x["src"] for x in c})
    lines = []
    hdr = f"- **Proposed Person: {names[0]}**"
    if len(names) > 1: hdr += f"  (also seen as: {', '.join(names[1:])})"
    lines.append(hdr)
    st = resolve_status(srcs)
    dt = variants(c, "Disengagement Type")
    dtxt = f"  ·  Disengagement Type {render_variants(dt)}" if dt else ("  ·  Disengagement Type Archived (proposed)" if st == "Archived" else "")
    lines.append(f"  - Status **{st}**{dtxt}  ·  History Flags {srcs}")
    em = emails_union(c)
    if em:
        lines.append(f"  - Emails: {em[0]} (primary)" + (", " + ", ".join(em[1:]) if len(em) > 1 else ""))
    ghs = sorted({x["f"].get("GitHub Handle", "").strip() for x in c if x["f"].get("GitHub Handle")})
    if ghs: lines.append(f"  - GitHub: {', '.join(ghs)}")
    # placements against the three-column team model
    cops = sorted({v for x in c for v in x["cop"]})
    if cops: lines.append(f"  - Communities of Practice (link): {', '.join(cops)}")
    rteams = sorted({roster_team(x["notes"]) for x in c if roster_team(x["notes"])})
    if rteams: lines.append(f"  - Product Teams (from 2024 roster hint, verify): {', '.join(rteams)}")
    slack = sorted({m.group(1).strip() for x in c for m in [re.search(r'Most recent Slack channel:\s*(.+)', x['notes'])] if m})
    if slack: lines.append(f"  - Slack-channel evidence (not membership): {', '.join(slack)}")
    # every other populated field, provenance-tagged, nothing dropped
    keys = [k for k in PREF] + sorted({k for x in c for k in x["f"] if k not in SPECIAL and k not in PREF})
    seen_keys = set()
    for k in keys:
        if k in seen_keys: continue
        seen_keys.add(k)
        vv = variants(c, k)
        if vv: lines.append(f"  - {k}: {render_variants(vv)}")
    # notes carry the real narrative (intros, contact info, actions) — keep them, per source
    notelines = []
    for x in c:
        nt = (x["f"].get("Notes") or "").strip()
        if nt: notelines.append(f"    - [{x['src']}] " + nt.replace("\n", "; "))
    if notelines:
        lines.append("  - Notes (union):")
        lines += notelines
    return lines

out = ["---", "tags:", "  - open-austin", "  - vrm", "  - import", "---",
       "# VRM Dedup Approval Slate", "",
       "Piece-by-piece merge proposals for collapsing Intake Staging into People. Companion to [vrm-import-normalization.md](vrm-import-normalization.md). Base `applWRIFU0rPBIgTe`, Intake Staging `tbldmJXE2WnvSX6xD`, People `tblWu2q7Zmkx4Lsz6`.",
       "",
       "How to use: go through each **M#**. The indented **Proposed Person** block is the full merged union of every populated field across the listed rows (emails, GitHub handles, skills text, availability, activity, notes) — that is what the promoted People record should hold, so eyeball it before approving. Placements map onto the three team columns: CoP values become **Communities of Practice** links, the 2024 roster hint is a **Product Teams** candidate (verify, it's stale), and a Slack channel is evidence, not membership. On approve: create ONE People record from the union, accrue all History Flags, set the status, pick one UUID, then delete/flag the merged staging rows. `high` = rows share an email or GitHub handle; `review` = matched on name only.",
       "", f"Generated 2026-08-11: **{len(merges)} merge clusters**, **{len(singles)} singletons**, from 189 staged rows.", ""]
for n, c in enumerate(merges, 1):
    conf = "high" if strong(c) else "review (name-only match)"
    names = sorted({x["name"] for x in c})
    out.append(f"### M{n} — {names[0]}  ({conf})")
    out.append(f"Merging {len(c)} staging rows:")
    for x in c:
        out.append(f"- `{x['id']}` [{x['src']}] {x['name']} | {x['email'] or '-'} | gh:{x['gh'] or '-'}{team_hint(x['notes'])}")
    out += proposed_block(c)
    out.append("- Decision: [ ] approve merge  [ ] keep separate  [ ] needs review")
    out.append("")
out.append("## Singletons (promote 1:1, no merge decision)")
out.append("Each becomes a People record as-is; nothing to merge. `id | source | email | gh | status`.")
for x in sorted(singles, key=lambda x: x["name"].lower()):
    out.append(f"- {x['name']} | `{x['id']}` | [{x['src']}] | {x['email'] or '-'} | gh:{x['gh'] or '-'} | {x['status']}{team_hint(x['notes'])}")
open(sys.argv[1], "w").write("\n".join(out))
print(f"{len(merges)} merge clusters, {len(singles)} singletons -> {sys.argv[1]}")
