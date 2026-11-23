import os, time
from playwright.sync_api import sync_playwright
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
url = "file:///" + os.path.join(root, "index.html").replace("\\", "/") + "?demo=1"
errs=[]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto(url); t=time.time()
    pg.wait_for_selector(".end", timeout=40000); print("demo reached end in %.1fs"%(time.time()-t))
    pg.wait_for_timeout(600); pg.screenshot(path=os.path.join(root,"screenshots","demo-end.png"))
    print(pg.inner_text(".stats").replace("\n"," "), errs); b.close()
