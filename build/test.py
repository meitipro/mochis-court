import sys, os, json
from playwright.sync_api import sync_playwright
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
url = "file:///" + os.path.join(root, "index.html").replace("\\", "/")
shots = os.path.join(root, "screenshots")
errors = []
def run(p, name, w, h, mobile):
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mobile else 1, has_touch=mobile, is_mobile=mobile)
    pg = ctx.new_page()
    pg.on("console", lambda m: errors.append((name, m.text)) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append((name, str(e))))
    pg.goto(url + "?seed=7"); pg.wait_for_timeout(500)
    pg.screenshot(path=f"{shots}/{name}-1-title.png")
    pg.click("#howBtn"); pg.wait_for_timeout(100); pg.screenshot(path=f"{shots}/{name}-1b-howitworks.png")
    pg.click("#startBtn"); pg.wait_for_timeout(500); pg.screenshot(path=f"{shots}/{name}-2-tutorial.png")
    pg.click("#skip"); pg.wait_for_timeout(500)
    # force case order: flip case first, so the appeal can flip; then random rest
    pg.evaluate("""()=>{const f=CASES.find(c=>c.id===19);S.cases=[f,...S.cases.filter(c=>c.id!==19).slice(0,TOTAL-1)];showCase()}""")
    pg.wait_for_timeout(500)
    overflow = []
    def check(tag):
        r = pg.evaluate("""()=>({sh:document.documentElement.scrollHeight,ih:innerHeight,sw:document.documentElement.scrollWidth,iw:innerWidth,
          stage:(()=>{const s=document.querySelector('.screen');return s?[s.scrollHeight,s.clientHeight]:null})(),
          sheet:(()=>{const s=document.querySelector('#sheet');return s?[s.scrollHeight,s.clientHeight]:null})()})""")
        overflow.append((tag, r))
    pg.screenshot(path=f"{shots}/{name}-3-case.png"); check("case0")
    appealed = False
    for i in range(8):
        info = pg.evaluate("()=>({v:S.cur.validators,id:S.cur.id})")
        maj = "A" if info["v"].count("A") >= 2 else "B"
        if i == 0:  # go against the first jury majority (player = B, truth side after appeal)
            vote = "B"
        elif i == 1:  # a loss with no appeal chance? appeal already used -> shows no button
            vote = "A" if maj == "B" else "B"
        else:
            vote = maj
        pg.keyboard.press("ArrowLeft" if vote == "A" else "ArrowRight")
        pg.wait_for_selector("#sheet", timeout=8000)
        if i == 0:
            pg.screenshot(path=f"{shots}/{name}-4-verdict-lose.png"); check("verdict0")
            assert pg.query_selector("#appealBtn"), "appeal button missing"
            pg.keyboard.press("a")
            pg.wait_for_function("/APPEAL VERDICT/.test(document.querySelector('#banner').textContent)", timeout=8000)
            pg.wait_for_timeout(300)
            pg.screenshot(path=f"{shots}/{name}-5-appeal.png"); check("appeal")
            gen = pg.inner_text("#gen"); print(name, "gen after appeal flip:", gen)
        if i == 2:
            pg.screenshot(path=f"{shots}/{name}-4b-verdict-win.png")
        if i == 1:
            assert not pg.query_selector("#appealBtn"), "second appeal must not be offered"
        pg.keyboard.press("Enter"); pg.wait_for_timeout(450)
    pg.wait_for_selector("#again", timeout=5000); pg.wait_for_timeout(500)
    pg.screenshot(path=f"{shots}/{name}-6-end.png"); check("end")
    print(name, "end:", pg.inner_text(".stats").replace("\n", " "), "|", pg.inner_text("#rank"))
    pg.click("#copyBtn"); pg.wait_for_timeout(200); print(name, "copy:", pg.inner_text("#copyOut"))
    print(name, "best saved:", pg.evaluate("localStorage.getItem('mochi.best')"))
    for t, r in overflow: print(name, t, json.dumps(r))
    # timeout path
    pg.goto(url + "?seed=3"); pg.click("#startBtn"); pg.click("#skip"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{S.t0-=14500}"); pg.wait_for_selector("#sheet", timeout=6000)
    print(name, "timeout:", pg.inner_text("#res"))
    # storage failure
    pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
    pg.goto(url); pg.click("#startBtn"); pg.click("#skip"); pg.wait_for_timeout(300)
    b.close()
with sync_playwright() as p:
    run(p, "mobile-390x844", 390, 844, True)
    run(p, "desktop-1280x720", 1280, 720, False)
print("console/page errors:", errors)
