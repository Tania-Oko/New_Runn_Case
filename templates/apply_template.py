#!/usr/bin/env python3
"""Create a Runn project from a template JSON in this folder.
Usage: apply_template.py TEMPLATE.json "Project name" CLIENT_ID TAG_ID START_MONDAY(YYYY-MM-DD)
Needs RUNN_API_TOKEN. Creates a NEW project only; never edits existing ones.
START_MONDAY must be today or the Monday of the current week (no historic time)."""
import json, os, sys, urllib.request
from datetime import date, timedelta

H = {"User-Agent": "fideres-runn-setup/1.0", "Authorization": "Bearer " + os.environ["RUNN_API_TOKEN"],
     "Accept-Version": "1.0.0", "Content-Type": "application/json"}

def call(method, path, body=None):
    req = urllib.request.Request("https://api.runn.io" + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None, headers=H)
    with urllib.request.urlopen(req) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else None

tpl = json.load(open(sys.argv[1]))
name, client, tag, start = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), date.fromisoformat(sys.argv[5])
day = lambda n: (start + timedelta(days=n)).isoformat()

p = tpl["project"]
proj = call("POST", "/projects/", {"name": name, "clientId": client, **p})
pid = proj["id"]
call("PATCH", f"/projects/{pid}", {"tags": [{"id": tag}]})
phase_ids = {}
for ph in tpl["phases"]:
    r = call("POST", f"/projects/{pid}/phases", {"name": ph["name"], "color": ph["color"],
             "startDate": day(ph["startOffsetDays"]), "endDate": day(ph["endOffsetDays"])})
    phase_ids[ph["name"]] = r["id"]
for m in tpl["milestones"]:
    call("POST", f"/projects/{pid}/milestones", {"title": m["title"], "icon": m["icon"], "date": day(m["dateOffsetDays"]), "note": m.get("note") or ""})
# Runn placeholders belong to one project only, so create one per template placeholder.
ph_map = {}
for a in tpl["assignments"]:
    k = a["placeholderPersonId"]
    if k not in ph_map:
        ph_map[k] = call("POST", "/placeholders/", {"roleId": a["roleId"]})["id"]
for a in tpl["assignments"]:
    call("POST", "/assignments", {"personId": ph_map[a["placeholderPersonId"]], "projectId": pid, "roleId": a["roleId"],
         "phaseId": phase_ids[a["phase"]], "minutesPerDay": a["minutesPerDay"], "isBillable": a["isBillable"],
         "startDate": day(a["startOffsetDays"]), "endDate": day(a["endOffsetDays"])})
print(pid)
