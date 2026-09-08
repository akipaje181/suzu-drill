#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""テストの読み取り結果を index.html の PAGES_PRESET に追加する（iPad は次回起動時に取り込む）。

使い方:
  python3 tools_add_page.py "9/12 小テスト 1-⑧" dochira:x aida:o sorezore:x nagasa_hiki:o kago:o [--date 2026-09-12] [--push]

  型:o = 正解 / 型:x = 不正解 / 型:? = 不明（記録には入れない）
  型のキーは index.html の var TYPES にあるもの（dochira, aida, wa, sorezore, kago, ...）
  --push を付けると sw.js の版を上げて commit / push まで行う。
"""
import sys, re, io, json, random, datetime, subprocess, pathlib
HERE = pathlib.Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = {a.split("=")[0]: (a.split("=")[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
if len(args) < 2:
    print(__doc__); sys.exit(1)
label, specs = args[0], args[1:]
date = opts.get("--date") or datetime.date.today().isoformat()
if "--date" in opts and opts["--date"] is True:   # "--date 2026-09-12" の形
    i = sys.argv.index("--date"); date = sys.argv[i + 1]; specs = [x for x in specs if x != date]

html = io.open(HERE / "index.html", encoding="utf-8").read()
types = json.loads(re.search(r"^  var TYPES = (\{.*\});$", html, re.M).group(1))
problems = []
for n, sp in enumerate(specs, 1):
    key, _, res = sp.partition(":")
    if key not in types: sys.exit("知らない型: %s（使える型: %s）" % (key, " ".join(types)))
    ok = True if res in ("o", "ok", "○") else False if res in ("x", "ng", "✗") else None
    problems.append({"no": n, "key": key, "ok": ok})
page = {"id": "p_%s_%04x" % (date.replace("-", ""), random.randrange(65536)), "label": label,
        "at": date + "T12:00:00", "seed": random.randrange(1, 2**31 - 1), "problems": problems}
m = re.search(r"^  var PAGES_PRESET = (\[.*\]);$", html, re.M)
arr = json.loads(m.group(1)); arr.append(page)
html = html[:m.start()] + "  var PAGES_PRESET = " + json.dumps(arr, ensure_ascii=False, separators=(",", ":")) + ";" + html[m.end():]
io.open(HERE / "index.html", "w", encoding="utf-8").write(html)
print("追加: %s  (%s)  %d問  ✗=%s" % (page["label"], page["id"], len(problems), ",".join(types[p["key"]]["name"] for p in problems if p["ok"] is False) or "なし"))

sw = io.open(HERE / "sw.js", encoding="utf-8").read()
ver = int(re.search(r"suzu-drill-v(\d+)", sw).group(1))
io.open(HERE / "sw.js", "w", encoding="utf-8").write(sw.replace("suzu-drill-v%d" % ver, "suzu-drill-v%d" % (ver + 1)))
print("sw.js: v%d -> v%d" % (ver, ver + 1))
if opts.get("--push"):
    subprocess.check_call(["git", "-C", str(HERE), "add", "-A"])
    subprocess.check_call(["git", "-C", str(HERE), "commit", "-q", "-m", "テストのページを追加: %s\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" % label])
    subprocess.check_call(["git", "-C", str(HERE), "push", "-q", "origin", "main"])
    print("push 済み（数十秒で iPad に反映）")
