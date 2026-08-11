#!/usr/bin/env python3
"""Read-first Airtable CLI for Open Austin (airtable-tooling spike).

Stdlib only (urllib) so there is no dependency to install. Auth comes from the
AIRTABLE_TOKEN environment variable (loaded from the gitignored .env by run.sh).
Never prints the token. Read commands only in Phase 1.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.airtable.com/v0"


def _token():
    tok = os.environ.get("AIRTABLE_TOKEN", "").strip()
    if not tok:
        sys.exit("AIRTABLE_TOKEN is not set (expected in the gitignored .env).")
    return tok


def api_get(path, params=None):
    url = f"{API}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {_token()}"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limited
                time.sleep(1.5)
                continue
            body = e.read().decode("utf-8", "replace")
            sys.exit(f"HTTP {e.code} on {path}: {body}")
    sys.exit(f"rate-limited repeatedly on {path}")


def api_post(path, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API}/{path}", data=data, method="POST",
        headers={"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as r:
                return True, json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5)
                continue
            return False, e.read().decode("utf-8", "replace")
    return False, "rate-limited repeatedly"


def cmd_import_records(base_id, table_id, recfile, execute=False):
    """Insert records from a JSON array of field-dicts. Dry-run unless execute=True.
    Batches of 10 (Airtable limit); typecast lets Airtable coerce dates/selects."""
    recs = json.load(open(recfile))
    print(f"{'IMPORT' if execute else 'DRY-RUN'}: {len(recs)} records into {table_id}")
    if recs:
        print("sample:", json.dumps(recs[0], ensure_ascii=False)[:500])
    if not execute:
        print("re-run with --execute to insert.")
        return
    created = 0
    for i in range(0, len(recs), 10):
        batch = {"records": [{"fields": r} for r in recs[i:i + 10]], "typecast": True}
        ok, res = api_post(f"{base_id}/{urllib.parse.quote(table_id)}", batch)
        if ok:
            created += len(res.get("records", []))
        else:
            print(f"  FAIL at batch {i}: {res[:300]}")
            break
        time.sleep(0.3)
    print(f"created {created} records.")


def cmd_apply_fields(specfile, execute=False):
    """Create fields from a JSON spec: {"baseId","tables":[{"id","name","fields":[{name,type,options?}]}]}.
    Idempotent: skips fields that already exist by name. Dry-run unless execute=True."""
    spec = json.load(open(specfile))
    base_id = spec["baseId"]
    current = {t["id"]: {f["name"] for f in t.get("fields", [])} for t in base_schema(base_id)}
    created = skipped = failed = 0
    for tbl in spec["tables"]:
        exist = current.get(tbl["id"], set())
        for fld in tbl["fields"]:
            if fld["name"] in exist:
                skipped += 1
                continue
            if not execute:
                print(f"  PLAN  {tbl['name']}.{fld['name']}  ({fld['type']})")
                created += 1
                continue
            body = {"name": fld["name"], "type": fld["type"]}
            if fld.get("options"):
                body["options"] = fld["options"]
            ok, res = api_post(f"meta/bases/{base_id}/tables/{tbl['id']}/fields", body)
            if ok:
                print(f"  OK    {tbl['name']}.{fld['name']}")
                created += 1
            else:
                print(f"  FAIL  {tbl['name']}.{fld['name']}: {res}")
                failed += 1
            time.sleep(0.25)
    verb = "created" if execute else "to create"
    print(f"\n{created} fields {verb}, {skipped} already existed, {failed} failed.")


def list_bases():
    bases, offset = [], None
    while True:
        params = {"offset": offset} if offset else None
        data = api_get("meta/bases", params)
        bases.extend(data.get("bases", []))
        offset = data.get("offset")
        if not offset:
            break
    return bases


def base_schema(base_id):
    return api_get(f"meta/bases/{base_id}/tables").get("tables", [])


def all_records(base_id, table_id, cap=2000):
    recs, offset = [], None
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        data = api_get(f"{base_id}/{urllib.parse.quote(table_id)}", params)
        recs.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset or len(recs) >= cap:
            break
    return recs


def cmd_list_bases():
    for b in list_bases():
        print(f"{b['id']}\t{b.get('permissionLevel','?')}\t{b['name']}")


def cmd_tables(base_id):
    for t in base_schema(base_id):
        fields = ", ".join(f["name"] for f in t.get("fields", []))
        views = ", ".join(v["name"] for v in t.get("views", []))
        print(f"\n## {t['name']}  (id={t['id']})")
        print(f"fields: {fields}")
        print(f"views:  {views}")


def cmd_records(base_id, table_id, limit=5):
    recs = all_records(base_id, table_id, cap=int(limit))
    for r in recs[: int(limit)]:
        print(json.dumps(r.get("fields", {}), ensure_ascii=False))


def cmd_csv(base_id, table_id):
    import csv as _csv
    tables = base_schema(base_id)
    match = next((t for t in tables if t["id"] == table_id or t["name"] == table_id), None)
    cols = [f["name"] for f in match["fields"]] if match else []
    recs = all_records(base_id, table_id)
    if not cols:
        seen = []
        for r in recs:
            for k in r.get("fields", {}):
                if k not in seen:
                    seen.append(k)
        cols = seen
    w = _csv.writer(sys.stdout)
    w.writerow(cols)
    for r in recs:
        f = r.get("fields", {})
        w.writerow([json.dumps(f[c], ensure_ascii=False) if isinstance(f.get(c), (list, dict)) else f.get(c, "") for c in cols])


def cmd_survey():
    """Full read: every base, its tables, field names, record counts, 1 sample."""
    for b in list_bases():
        print(f"\n{'='*70}\nBASE: {b['name']}  (id={b['id']}, {b.get('permissionLevel','?')})")
        for t in base_schema(b["id"]):
            recs = all_records(b["id"], t["id"])
            n = len(recs)
            fields = ", ".join(f["name"] for f in t.get("fields", []))
            print(f"\n  TABLE: {t['name']}  [{n} records]")
            print(f"    fields: {fields}")
            if recs:
                sample = recs[0].get("fields", {})
                s = json.dumps(sample, ensure_ascii=False)
                print(f"    sample: {s[:400]}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: airtable.py {list-bases|tables <base>|records <base> <table> [n]|survey}")
    cmd = args[0]
    if cmd == "list-bases":
        cmd_list_bases()
    elif cmd == "tables":
        cmd_tables(args[1])
    elif cmd == "records":
        cmd_records(args[1], args[2], args[3] if len(args) > 3 else 5)
    elif cmd == "apply-fields":
        cmd_apply_fields(args[1], execute=("--execute" in args))
    elif cmd == "import-records":
        cmd_import_records(args[1], args[2], args[3], execute=("--execute" in args))
    elif cmd == "csv":
        cmd_csv(args[1], args[2])
    elif cmd == "survey":
        cmd_survey()
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
