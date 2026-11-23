import base64, io, json, re, sys, os
from PIL import Image
src = sys.argv[1]
def enc(path, maxh, q=None):
    i = Image.open(path).convert("RGBA")
    if i.height > maxh:
        i = i.resize((round(i.width*maxh/i.height), maxh), Image.LANCZOS)
    b = io.BytesIO(); i.save(b, "WEBP", quality=82, method=6)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
out = {"mochi": enc(f"{src}/mochi-full-render.png", 640)}
for s in ["cookie","idea","love","stonks-down","stonks-up"]:
    out[s] = enc(f"{src}/mochi-sticker-{s}.png", 320)
logo = os.path.join(os.path.dirname(__file__), "GenLayer_Logo_White_2048.png")
if os.path.exists(logo):
    out["logo"] = enc(logo, 256); out["logoKind"] = "png"
else:
    t = open("D:/genlayer-arcade/components/GenLogo.tsx", encoding="utf8").read()
    paths = re.search(r'<g transform=.*?</g>', t, re.S).group(0)
    out["logo"] = '<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">' + paths.replace("currentColor", "#fff") + "</svg>"
    out["logoKind"] = "svg"
json.dump(out, open(os.path.join(os.path.dirname(__file__), "assets.json"), "w"))
print({k: len(v) for k, v in out.items()})
