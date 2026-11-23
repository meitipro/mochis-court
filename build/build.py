import json, os
d = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(d, "assets.json")))
t = open(os.path.join(d, "template.html"), encoding="utf8").read()
t = t.replace("/*ASSETS*/", "const ASSETS = " + json.dumps(a) + ";")
out = os.path.join(d, "..", "index.html")
open(out, "w", encoding="utf8").write(t)
print(os.path.getsize(out) // 1024, "KB")
