#!/usr/bin/env python3
"""Build the full operations-assessment field instrument.

Parses the three assessment layers from their source files:
  - Enterprise failure modes (OFM-*) from checklist.yaml
  - Process failure modes (PFM-*) from 11-16 function files (all 88 processes)
  - Role failure patterns (RFM-*) from 17-role-assessment.md

and emits:
  - field-instrument.yaml  (machine-readable: every item with prompt/signals,
    score 0/1/2 + notes fields, grouped by layer/domain/process/role)
  - field-instrument.html  (self-contained interactive scoring instrument:
    search, section nav, 0/1/2 segmented scoring with notes, progress,
    save/open state as JSON, export scored YAML)

The markdown/YAML sources remain the source of truth — rerun after any edit.
Usage: python3 build_field_instrument.py
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

HERE = Path(__file__).parent
ROOT = HERE.parent

FN_FILES = ["11-fn-patient-access.md", "12-fn-mid-cycle.md", "13-fn-claims-payments.md",
            "14-fn-denials-ar.md", "15-fn-patient-financial.md", "16-fn-enterprise.md"]


def process_names():
    tax = (ROOT / "00-master-taxonomy.md").read_text()
    return dict(re.findall(r"\*\*(\d{1,2}\.\d)\s+([^*]+?)\*\*", tax))


def parse_ofm():
    doc = yaml.safe_load((HERE / "checklist.yaml").read_text())
    items = []
    for domain, entries in doc.items():
        for oid, e in entries.items():
            items.append({"id": oid, "layer": "enterprise",
                          "group": domain.replace("_", " ").title(),
                          "prompt": e["prompt"], "signals": "", "practice": ""})
    return items


def parse_pfm():
    pnames = process_names()
    items = []
    for fname in FN_FILES:
        text = (HERE / fname).read_text()
        for m in re.finditer(
                r"^\| (PFM-(\d{1,2}\.\d)-\d\d) \| (.*?) \| (.*?) \| (.*?) \|\s*$",
                text, re.M):
            pid, proc, failure, signals, practice = m.groups()
            items.append({"id": pid, "layer": "process",
                          "group": f"{proc} {pnames.get(proc, '').strip()}".strip(),
                          "prompt": failure.strip(), "signals": signals.strip(),
                          "practice": practice.strip()})
    return items


def parse_rfm():
    text = (HERE / "17-role-assessment.md").read_text()
    items = []
    for row in re.finditer(r"^\| \*\*(ROLE-[^*]+?)\*\*([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|",
                           text, re.M):
        role = row.group(1).strip()
        rfm_cell, rbp_cell = row.group(4), row.group(5)
        parts = re.split(r";\s*(?=RFM-)", rfm_cell.strip())
        for part in parts:
            pm = re.match(r"(RFM-[A-Z]+-\d\d)\s+(.*)", part.strip())
            if pm:
                items.append({"id": pm.group(1), "layer": "role", "group": role,
                              "prompt": pm.group(2).strip(), "signals": "",
                              "practice": rbp_cell.strip()})
    return items


def build_yaml(items):
    out = {"instrument": "revenue-cycle operations assessment — field instrument",
           "scoring": "0 = not observed, 1 = partial/suspected, 2 = clearly present (evidence required)",
           "layers": {}}
    for it in items:
        layer = out["layers"].setdefault(it["layer"], {})
        group = layer.setdefault(it["group"], {})
        entry = {"prompt": it["prompt"], "score": 0, "notes": ""}
        if it["signals"]:
            entry["signals"] = it["signals"]
        group[it["id"]] = entry
    return out


HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RCM Operations Assessment — Field Instrument</title>
<style>
  :root { --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
    --grid:#e1e0d9; --baseline:#c3c2b7; --ring:rgba(11,11,11,0.10);
    --seq:#2a78d6; --warning-ink:#7a5200; --critical-ink:#d03b3b; --good-ink:#006300; }
  @media (prefers-color-scheme: dark) {
    :root { --page:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink-2:#c3c2b7; --grid:#2c2c2a;
      --baseline:#383835; --ring:rgba(255,255,255,0.10); --seq:#3987e5;
      --warning-ink:#fab219; --critical-ink:#d03b3b; --good-ink:#0ca30c; } }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--page); color:var(--ink);
         font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }
  header { position:sticky; top:0; z-index:10; background:var(--page);
           border-bottom:1px solid var(--grid); padding:12px 20px; }
  .hrow { display:flex; gap:12px; align-items:center; flex-wrap:wrap; max-width:1200px; margin:0 auto; }
  h1 { font-size:16.5px; margin:0; white-space:nowrap; }
  #q { flex:1; min-width:180px; max-width:380px; background:var(--surface); color:var(--ink);
       border:1px solid var(--ring); border-radius:999px; padding:7px 14px; font:inherit; }
  .btn { border:1px solid var(--ring); background:var(--surface); color:var(--ink);
         border-radius:8px; padding:6px 12px; font:inherit; font-size:12.5px; font-weight:600; cursor:pointer; }
  .prog { color:var(--muted); font-size:12px; white-space:nowrap; }
  .tabs { display:flex; gap:6px; }
  .tabs button { border:1px solid var(--ring); background:var(--surface); color:var(--ink-2);
       border-radius:999px; padding:5px 13px; font:inherit; font-size:12.5px; font-weight:600; cursor:pointer; }
  .tabs button[aria-selected="true"] { color:var(--ink); border-color:var(--baseline);
       box-shadow:inset 0 0 0 1px var(--baseline); }
  main { max-width:1200px; margin:0 auto; padding:16px 20px 80px; }
  .intro { color:var(--ink-2); font-size:13px; margin:6px 0 16px; }
  h2 { font-size:14px; margin:26px 0 8px; color:var(--ink); position:sticky; top:57px;
       background:var(--page); padding:6px 0; z-index:5; border-bottom:1px solid var(--grid); }
  .item { display:grid; grid-template-columns:1fr auto; gap:6px 14px; padding:10px 10px;
          border-bottom:1px solid var(--grid); border-radius:8px; align-items:start; }
  .item:hover { background:var(--grid); }
  .item.scored-1 { border-left:3px solid var(--warning-ink); }
  .item.scored-2 { border-left:3px solid var(--critical-ink); }
  .item .p { font-size:13px; color:var(--ink-2); }
  .item .p b { color:var(--ink); font-weight:600; }
  .item .sig { font-size:12px; color:var(--muted); margin-top:2px; }
  .item .fix { font-size:12px; color:var(--muted); margin-top:2px; display:none; }
  .item.scored-1 .fix, .item.scored-2 .fix { display:block; }
  .fix b { color:var(--good-ink); font-weight:600; }
  .seg { display:flex; gap:4px; }
  .seg button { border:1px solid var(--ring); background:var(--surface); color:var(--muted);
       border-radius:6px; padding:3px 10px; font:inherit; font-size:12px; cursor:pointer; white-space:nowrap; }
  .seg button[aria-pressed="true"] { color:var(--ink); font-weight:700; border-color:var(--baseline);
       box-shadow:inset 0 0 0 1px var(--baseline); }
  .note { grid-column:1 / -1; }
  .note input { width:100%; background:var(--surface); color:var(--ink); border:1px dashed var(--ring);
       border-radius:7px; padding:5px 9px; font:inherit; font-size:12.5px; }
  footer { max-width:1200px; margin:0 auto; padding:10px 20px 40px; color:var(--muted); font-size:12px; }
  input[type=file] { display:none; }
</style></head>
<body>
<header><div class="hrow">
  <h1>Operations Assessment — Field Instrument</h1>
  <span class="prog" id="prog"></span>
  <input id="q" type="search" placeholder="Search items, signals, IDs…">
  <div class="tabs" id="tabs">
    <button data-l="enterprise" aria-selected="true">Enterprise</button>
    <button data-l="process" aria-selected="false">Process</button>
    <button data-l="role" aria-selected="false">Role</button>
  </div>
  <button class="btn" id="save">Save…</button>
  <button class="btn" id="open">Open…</button>
  <button class="btn" id="exportY">Export YAML</button>
  <input type="file" id="fileIn" accept=".json">
</div></header>
<main>
  <p class="intro">Score each item <b>0 = not observed · 1 = partial/suspected · 2 = clearly
  present</b>. Evidence rule: a 2 requires a named artifact, a walked process, or two
  independent interviews — capture it in the note. Items scored 1–2 reveal their paired
  practice inline. Nothing leaves this page; save your state as JSON and export scored YAML
  for the reconciliation workflow (README: causal chains to facet scores and locked value).</p>
  <div id="body"></div>
</main>
<footer>Generated by build_field_instrument.py from checklist.yaml + the function and role
assessment files (operations-assessment/, files 01–17). Sources remain the source of truth —
regenerate after edits. Layer composition: OFM (enterprise) → PFM (process) → RFM (role);
prescriptions differ by layer (structure / standard work / coaching).</footer>
<script>
const ITEMS = __ITEMS__;
const S = { layer:"enterprise", q:"", scores:{}, notes:{} };
const esc = s => String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function render(){
  const q = S.q.toLowerCase();
  const rows = ITEMS.filter(i => i.layer===S.layer &&
    (!q || (i.id+" "+i.group+" "+i.prompt+" "+i.signals).toLowerCase().includes(q)));
  let html = "", g = null;
  for (const i of rows){
    if (i.group!==g){ g=i.group; html+=`<h2>${esc(g)}</h2>`; }
    const sc = S.scores[i.id]||0;
    html += `<div class="item scored-${sc}" data-id="${i.id}">
      <div><div class="p"><b>${i.id}</b> — ${esc(i.prompt)}</div>
        ${i.signals?`<div class="sig">Signals: ${esc(i.signals)}</div>`:""}
        ${i.practice?`<div class="fix"><b>Paired practice:</b> ${esc(i.practice)}</div>`:""}</div>
      <div class="seg" data-id="${i.id}">
        ${[0,1,2].map(v=>`<button data-v="${v}" aria-pressed="${sc===v}">${["Not obs.","Partial","Present"][v]}</button>`).join("")}
      </div>
      <div class="note"><input placeholder="Evidence / notes…" data-note="${i.id}" value="${esc(S.notes[i.id]||"")}"></div>
    </div>`;
  }
  document.getElementById("body").innerHTML = html || `<p class="intro">No items match.</p>`;
  progress();
}
function progress(){
  const per = l => { const its=ITEMS.filter(i=>i.layer===l);
    const done=its.filter(i=>(S.scores[i.id]||0)>0).length;
    const p2=its.filter(i=>S.scores[i.id]===2).length;
    return `${l}: ${done}/${its.length} flagged (${p2} present)`; };
  document.getElementById("prog").textContent =
    ["enterprise","process","role"].map(per).join(" · ");
}
document.addEventListener("click", e=>{
  const b = e.target.closest(".seg button");
  if (b){ const id=b.parentElement.dataset.id; S.scores[id]=+b.dataset.v;
    const item=b.closest(".item"); item.className=`item scored-${S.scores[id]}`;
    for (const x of b.parentElement.children) x.setAttribute("aria-pressed", x===b);
    progress(); persist(); return; }
  const t = e.target.closest(".tabs button");
  if (t){ S.layer=t.dataset.l;
    for (const x of document.querySelectorAll(".tabs button")) x.setAttribute("aria-selected",x===t);
    render(); }
});
document.addEventListener("input", e=>{
  if (e.target.dataset?.note){ S.notes[e.target.dataset.note]=e.target.value; persist(); }
  if (e.target.id==="q"){ S.q=e.target.value; render(); }
});
function persist(){ try{ localStorage.setItem("rcm-field-instrument", JSON.stringify({scores:S.scores,notes:S.notes})); }catch(e){} }
try{ const saved=JSON.parse(localStorage.getItem("rcm-field-instrument")||"null");
  if (saved){ S.scores=saved.scores||{}; S.notes=saved.notes||{}; } }catch(e){}
document.getElementById("save").onclick = ()=>{
  const blob=new Blob([JSON.stringify({scores:S.scores,notes:S.notes},null,1)],{type:"application/json"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob);
  a.download="field-instrument-state.json"; a.click(); };
document.getElementById("open").onclick = ()=>document.getElementById("fileIn").click();
document.getElementById("fileIn").onchange = async e=>{
  const f=e.target.files[0]; if(!f) return;
  const d=JSON.parse(await f.text()); S.scores=d.scores||{}; S.notes=d.notes||{}; render(); persist(); };
document.getElementById("exportY").onclick = ()=>{
  const lines=["# field instrument scores — generated export",
    "# 0 = not observed, 1 = partial, 2 = clearly present"];
  let layer=null, group=null;
  for (const i of ITEMS){
    if (i.layer!==layer){ layer=i.layer; lines.push(`${layer}:`); group=null; }
    if (i.group!==group){ group=i.group; lines.push(`  "${group}":`); }
    lines.push(`    ${i.id}: {score: ${S.scores[i.id]||0}${S.notes[i.id]?`, notes: "${(S.notes[i.id]||"").replace(/"/g,"'")}"`:""}}`);
  }
  const blob=new Blob([lines.join("\n")+"\n"],{type:"text/yaml"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob);
  a.download="field-instrument-scores.yaml"; a.click(); };
render();
</script></body></html>
"""


def main():
    items = parse_ofm() + parse_pfm() + parse_rfm()
    by_layer = {}
    for it in items:
        by_layer[it["layer"]] = by_layer.get(it["layer"], 0) + 1
    ids = [it["id"] for it in items]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        sys.exit(f"duplicate ids: {sorted(dupes)}")

    (HERE / "field-instrument.yaml").write_text(
        yaml.safe_dump(build_yaml(items), sort_keys=False, allow_unicode=True, width=110))
    (HERE / "field-instrument.html").write_text(HTML.replace("__ITEMS__", json.dumps(items)))
    print(f"field instrument built: {len(items)} items "
          f"({by_layer.get('enterprise',0)} enterprise OFM, {by_layer.get('process',0)} process PFM, "
          f"{by_layer.get('role',0)} role RFM) -> field-instrument.yaml / .html")


if __name__ == "__main__":
    main()
