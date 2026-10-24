import sys, json, urllib.parse, os
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3010/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/shots"
os.makedirs(OUT, exist_ok=True)

DEVICES = [
    ("android-360", 360, 740, 3, True),
    ("iphone-se-375", 375, 667, 2, True),
    ("iphone-14-390", 390, 844, 3, True),
    ("pixel-7-412", 412, 915, 2.625, True),
    ("iphone-max-430", 430, 932, 3, True),
    ("tablet-768", 768, 1024, 2, True),
    ("laptop-1024", 1024, 768, 1, False),
    ("laptop-1280", 1280, 800, 1, False),
    ("laptop-1366", 1366, 768, 1, False),
    ("desktop-1440", 1440, 900, 1, False),
    ("desktop-1920", 1920, 1080, 1, False),
]

problems = []
def bad(dev, msg):
    problems.append(f"[{dev}] {msg}")

FIRST_SCREEN_JS = """() => {
  const vh = innerHeight, r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {top:b.top, bottom:b.bottom, h:b.height}; };
  return {
    vh,
    overflow: Math.max(document.documentElement.scrollWidth, innerWidth) - (window.__devw || innerWidth),
    dock: (document.querySelector('.dock') || {}).getBoundingClientRect ? document.querySelector('.dock').getBoundingClientRect().height : 0,
    call: r('.top .round'),
    h1: r('#h1'),
    from: r('#heroPrice'),
    where: r('#brandCity'),
    img: r('.frame video, .frame img'),
    dockcall: r('.dock a[href^=tel]'),
    num: r('#topPhone'),
    frame: r('.frame'),
    rating: r('#heroRating'),
    head: (() => {
      const g = s => (document.querySelector(s) ? document.querySelector(s).getBoundingClientRect() : {width:0, left:0, right:0});
      const n = g('.topnav');
      return n.width ? {brand: g('.brand').right, navL: n.left, navR: n.right, act: g('.top-act').left} : null;
    })()
  };
}"""

TAP_JS = """() => {
  const out = [];
  document.querySelectorAll('a[href], button, .chip').forEach(e => {
    const b = e.getBoundingClientRect(), cs = getComputedStyle(e);
    if (!b.width || !b.height || cs.visibility === 'hidden' || e.closest('dialog:not([open])') || e.closest('[hidden]')) return;
    if (e.closest('.rev, footer, .revhead, .rating, .dl, .cookie, .fine, .f-grid, .replay-btn')) return;
    if (b.height < 44 || b.width < 44) out.push((e.className || e.tagName) + ' ' + (e.textContent||'').trim().slice(0,30) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height));
  });
  return out;
}"""

SMALLTEXT_JS = """() => {
  const out = new Set();
  document.querySelectorAll('body *').forEach(e => {
    if (!e.childNodes.length) return;
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return; const b = e.getBoundingClientRect(); if (!b.width) return;
    if (e.closest('dialog:not([open])') || e.closest('[hidden]')) return;
    const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 11.5) out.add(e.tagName + '.' + e.className + ' ' + fs);
  });
  return [...out];
}"""

with sync_playwright() as p:
    br = p.chromium.launch()
    for name, w, h, dpr, mobile in DEVICES:
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, locale="ru-RU")
        pg = ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url) if not (r.failure and "ERR_ABORTED" in str(r.failure)) else None)
        pg.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        pg.goto(URL, wait_until="networkidle")
        pg.evaluate(f"window.__devw={w}")
        fs = pg.evaluate(FIRST_SCREEN_JS)
        if fs["overflow"] > 0: bad(name, f"страница уезжает вбок на {fs['overflow']}px")
        if mobile:
            if not fs["img"] or fs["img"]["top"] > fs["vh"] * 0.6: bad(name, "первый экран: фото слишком низко")
            if w < 900 and (not fs["dockcall"] or fs["dockcall"]["bottom"] > fs["vh"] + 1): bad(name, "кнопка «Позвонить» внизу не видна")
        else:
            for k in ["h1", "from", "rating", "num", "frame"]:
                if not fs[k] or fs[k]["bottom"] > fs["vh"] + 1: bad(name, f"первый экран: «{k}» не виден без прокрутки ({fs[k]}, высота {fs['vh']})")
            hd = fs["head"]
            if w >= 1280 and not hd: bad(name, "меню разделов в шапке не показано")
            if hd and (hd["navL"] - hd["brand"] < 12 or hd["act"] - hd["navR"] < 12): bad(name, f"меню в шапке налезает на название или телефон: {hd}")
        taps = pg.evaluate(TAP_JS)
        if taps: bad(name, "мелкие кнопки: " + "; ".join(taps[:8]))
        small = pg.evaluate(SMALLTEXT_JS)
        if small: bad(name, "текст мельче 12px: " + "; ".join(small[:6]))
        pg.screenshot(path=f"{OUT}/{name}-first.png")
        hh = pg.evaluate("document.documentElement.scrollHeight")
        for yy in range(0, min(hh, 3000), 600):
            pg.evaluate(f"window.scrollTo(0,{yy})"); pg.wait_for_timeout(100)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(400)
        pg.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)
        if mobile and w < 900:
            pg.mouse.wheel(0, 1200); pg.wait_for_timeout(300)
            ov = pg.evaluate(f"Math.max(document.documentElement.scrollWidth, innerWidth) - {w}")
            if ov > 0: bad(name, f"после прокрутки страница уезжает вбок на {ov}px")
        if errors: bad(name, "ошибки в консоли: " + " | ".join(errors[:5]))
        if failed: bad(name, "не загрузилось: " + " | ".join(failed[:5]))
        ctx.close()

    # ---- 1. Тестирование бронирования окна ----
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="ru-RU")
    pg = ctx.new_page(); pg.goto(URL, wait_until="networkidle")
    def is_open(): return pg.evaluate("document.getElementById('sheet') ? document.getElementById('sheet').open : false")
    
    slot_btn = pg.locator(".slot").first
    slot_btn.tap(); pg.wait_for_timeout(350)
    if not is_open(): bad("сценарий-окно", "окно заявки не открылось по клику на свободный слот")
    pg.screenshot(path=f"{OUT}/sheet-slot.png")
    pg.locator("#sheetCloseBtn").tap(); pg.wait_for_timeout(250)
    if is_open(): bad("сценарий-окно", "окно не закрылось крестиком")

    # ---- 2. Тестирование интерактивного калькулятора ----
    pg.locator("#pick").scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    suv_btn = pg.locator('[data-car="suv"]')
    suv_btn.tap(); pg.wait_for_timeout(250)
    total_text = pg.locator("#calcTotal").inner_text()
    if not total_text or "₽" not in total_text: bad("калькулятор", "сумма расчета не отображается")
    pg.screenshot(path=f"{OUT}/calc-suv.png")

    # ---- 3. Тестирование Before/After слайдера ----
    pg.locator("#packages").scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    ba_slider = pg.locator("#baSlider")
    if not ba_slider.count(): bad("слайдер", "блок Before/After слайдера не найден")
    pg.screenshot(path=f"{OUT}/ba-slider.png")

    # ---- 4. Тестирование персонализации Hi-Fi (?studio=hifi) ----
    pg.goto(URL + "?studio=hifi", wait_until="networkidle")
    brand_hifi = pg.locator("#brandName").inner_text()
    if "HI-FI" not in brand_hifi: bad("персонализация", f"ожидался бренд HI-FI, получено: {brand_hifi}")
    price_hifi = pg.locator("#heroPrice").inner_text()
    if "85" not in price_hifi: bad("персонализация", f"ожидалась цена от 85к для Hi-Fi, получено: {price_hifi}")

    # ---- 5. Тестирование чистого режима (?studio=tonertut&clean=1) ----
    pg.goto(URL + "?studio=tonertut&clean=1", wait_until="networkidle")
    sw_btn_count = pg.locator("#studioSwitcherBtn").count()
    if sw_btn_count != 0: bad("clean-mode", "в режиме clean=1 кнопка выбора студий не скрыта")

    # ---- 6. Тестирование politika.html ----
    pg.goto(URL + "politika.html?studio=bezskolov", wait_until="networkidle")
    p_title = pg.title()
    if "БезСколов" not in p_title: bad("политика", f"в заголовке политики нет названия студии: {p_title}")

    # ---- 7. Тестирование tula-50.html ----
    pg.goto(URL + "tula-50.html", wait_until="networkidle")
    cards_count = pg.locator(".card").count()
    if cards_count != 50: bad("каталог-50", f"ожидалось ровно 50 студий в каталоге, найдено: {cards_count}")

    ctx.close()
    br.close()

print("="*40)
print("ИТОГ ТЕСТИРОВАНИЯ:")
print("ПРОБЛЕМ:", len(problems))
for x in problems:
    print(" -", x)
print("="*40)

if problems:
    sys.exit(1)
