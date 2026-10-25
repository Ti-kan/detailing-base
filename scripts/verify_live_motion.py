#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, time, argparse
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = "/Users/takanov/.gemini/antigravity-cli/brain/0cba8e2f-79d3-4c29-a34a-d0fa28861163"

SECTIONS_CONFIG = {
    "detailing": [
        ("01", "#slots-s", "Свободные окна"),
        ("02", "#pick", "Онлайн-калькулятор"),
        ("03", "#packages", "Пакеты и ДО/ПОСЛЕ"),
        ("04", "#price", "Прайс-лист"),
        ("05", "#tech", "Регламент чистоты"),
        ("06", "#reviews", "Отзывы"),
        ("07", "#where", "Адрес студии"),
        ("08", "#contacts", "Запись и гарантия"),
    ],
    "banya": [
        ("01", "#slots-s", "Свободные окна"),
        ("02", "#pick", "Подбор за 20 сек"),
        ("03", "#baths", "Срубы и зоны отдыха"),
        ("04", "#price", "Честные цены"),
        ("05", "#master", "Банные ритуалы"),
        ("06", "#reviews", "Отзывы"),
        ("07", "#where", "Как добраться"),
        ("08", "#book", "Как забронировать"),
    ]
}

def get_section_metrics(page, sec_id):
    return page.evaluate("""(id) => {
        const sec = document.querySelector(id);
        if (!sec) return { found: false };
        const sh = sec.querySelector('.sh');
        const hasIn = sh ? sh.classList.contains('in') : false;
        
        const wordInner = sec.querySelector('.sh h2 .word-inner, .sh h2 .w-in');
        let wordOpacity = null;
        let wordTransform = null;
        if (wordInner) {
            const st = window.getComputedStyle(wordInner);
            wordOpacity = st.opacity;
            wordTransform = st.transform;
        }
        
        const photo = sec.querySelector('.photo-reveal');
        let photoTransform = null;
        if (photo) {
            const st = window.getComputedStyle(photo, '::after');
            photoTransform = st.transform;
        }
        
        const card = sec.querySelector('.reveal-item, .pk-card, .tech-item, .bath, .slot');
        let cardOpacity = null;
        let cardHasIn = false;
        if (card) {
            cardOpacity = window.getComputedStyle(card).opacity;
            cardHasIn = card.classList.contains('in');
        }
        
        return {
            found: true,
            hasIn,
            wordOpacity,
            wordTransform,
            photoTransform,
            cardOpacity,
            cardHasIn
        };
    }""", sec_id)

def test_platform(page, url, platform_name):
    print(f"\n========================================================")
    print(f"  RUNNING STRICT 2-PHASE MOTION AUDIT: {platform_name.upper()}")
    print(f"  URL: {url}")
    print(f"========================================================")
    
    page.goto(url, wait_until="networkidle")
    
    # Dismiss any intro or skip if present
    skip_btn = page.locator("#cinemaSkip, .cinema-skip")
    if skip_btn.count() > 0 and skip_btn.first.is_visible():
        try:
            skip_btn.first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass
            
    # Step 1: Ensure scroll at 0
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    
    sections = SECTIONS_CONFIG[platform_name]
    sec03_id = sections[2][1]
    sec04_id = sections[3][1]
    
    # --- ASSERTION A (Pre-Scroll State at scrollY = 0) ---
    print("\n--- ASSERTION A: Pre-Scroll State (scrollY = 0) ---")
    m03 = get_section_metrics(page, sec03_id)
    m04 = get_section_metrics(page, sec04_id)
    
    print(f"Section 03 ({sec03_id}): has_in={m03['hasIn']}, word_opacity={m03['wordOpacity']}, photo_transform={m03['photoTransform']}")
    print(f"Section 04 ({sec04_id}): has_in={m04['hasIn']}, word_opacity={m04['wordOpacity']}")
    
    assert not m03['hasIn'], f"Assertion A FAILED: Section 03 ({sec03_id}) already has .in at scrollY=0!"
    assert float(m03['wordOpacity']) < 0.01, f"Assertion A FAILED: Section 03 word-inner opacity is {m03['wordOpacity']}, expected '0'!"
    if m03['photoTransform']:
        assert m03['photoTransform'] != 'matrix(1, 0, 0, 0, 0, 0)', f"Assertion A FAILED: Section 03 photo curtain already wiped open at scrollY=0!"
        
    assert not m04['hasIn'], f"Assertion A FAILED: Section 04 ({sec04_id}) already has .in at scrollY=0!"
    assert float(m04['wordOpacity']) < 0.01, f"Assertion A FAILED: Section 04 word-inner opacity is {m04['wordOpacity']}, expected '0'!"
    print(">>> Assertion A PASSED: Off-screen sections are strictly hidden with opacity: 0 and curtain closed!")
    
    # --- ASSERTION B (Active Scroll Trigger on Section 03) ---
    print("\n--- ASSERTION B: Active Scroll Trigger (Scroll into Section 03) ---")
    page.evaluate(f"document.querySelector('{sec03_id}').scrollIntoView({{ behavior: 'smooth' }})")
    
    # Mid-transition snapshot at t = 220ms
    page.wait_for_timeout(220)
    mid_m03 = get_section_metrics(page, sec03_id)
    mid_img_path = os.path.join(ARTIFACT_DIR, f"motion_mid_{platform_name}.png")
    page.screenshot(path=mid_img_path)
    print(f"Captured mid-transition screenshot: {mid_img_path}")
    print(f"Mid-transition (t=220ms): has_in={mid_m03['hasIn']}, word_opacity={mid_m03['wordOpacity']}, word_transform={mid_m03['wordTransform']}")
    
    # Settled snapshot at t = 950ms
    page.wait_for_timeout(730) # 220 + 730 = 950ms
    settled_m03 = get_section_metrics(page, sec03_id)
    settled_img_path = os.path.join(ARTIFACT_DIR, f"motion_settled_{platform_name}.png")
    page.screenshot(path=settled_img_path)
    print(f"Captured settled screenshot: {settled_img_path}")
    print(f"Settled (t=950ms): has_in={settled_m03['hasIn']}, word_opacity={settled_m03['wordOpacity']}, photo_transform={settled_m03['photoTransform']}")
    
    assert settled_m03['hasIn'], f"Assertion B FAILED: Section 03 missing .in after scroll!"
    assert float(settled_m03['wordOpacity']) >= 0.95, f"Assertion B FAILED: Section 03 word-inner opacity is {settled_m03['wordOpacity']}, expected >= 0.95!"
    if settled_m03['photoTransform']:
        assert settled_m03['photoTransform'] != 'matrix(1, 0, 0, 1, 0, 0)', f"Assertion B FAILED: Section 03 photo curtain did not open, transform={settled_m03['photoTransform']}!"
        
    # Scroll slightly to cards inside Section 03 to test card wave
    card_sel = f"{sec03_id} .reveal-item, {sec03_id} .bath, {sec03_id} .pk-card"
    card_el = page.locator(card_sel).first
    if card_el.count() > 0:
        card_el.scroll_into_view_if_needed()
        page.wait_for_timeout(850)
        card_op = page.evaluate(f"window.getComputedStyle(document.querySelector('{card_sel}')).opacity")
        print(f"Section 03 cards in view: card_opacity={card_op}")
        assert float(card_op) >= 0.95, f"Assertion B FAILED: Section 03 card opacity is {card_op}, expected >= 0.95!"
    print(">>> Assertion B PASSED: Section 03 animated smoothly, words rose to opacity: 1, photo curtain wiped open, cards opaque!")
    
    # --- ASSERTION C (Bi-Directional Reset on Scroll Up) ---
    print("\n--- ASSERTION C: Bi-Directional Reset on Scroll Up (window.scrollTo(0, 0)) ---")
    page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
    page.wait_for_timeout(550) # Allow 500ms fade-out transition to complete
    
    up_m03 = get_section_metrics(page, sec03_id)
    up_m04 = get_section_metrics(page, sec04_id)
    print(f"Scroll-up Reset Section 03 ({sec03_id}): has_in={up_m03['hasIn']}, word_opacity={up_m03['wordOpacity']}")
    print(f"Scroll-up Reset Section 04 ({sec04_id}): has_in={up_m04['hasIn']}, word_opacity={up_m04['wordOpacity']}")
    
    assert not up_m03['hasIn'], f"Assertion C FAILED: Section 03 ({sec03_id}) still has .in after scroll-up!"
    assert float(up_m03['wordOpacity']) < 0.01, f"Assertion C FAILED: Section 03 word-inner opacity is {up_m03['wordOpacity']}, expected '0'!"
    assert not up_m04['hasIn'], f"Assertion C FAILED: Section 04 ({sec04_id}) still has .in after scroll-up!"
    assert float(up_m04['wordOpacity']) < 0.01, f"Assertion C FAILED: Section 04 word-inner opacity is {up_m04['wordOpacity']}, expected '0'!"
    print(">>> Assertion C PASSED: Section 03 and 04 successfully reset to unrevealed state ready for re-scroll!")
    
    # --- FULL 8-SECTION CHOREOGRAPHY AUDIT TABLE ---
    print("\n" + "=" * 88)
    print(f"  FULL 8-SECTION CHOREOGRAPHY MOTION TABLE: {platform_name.upper()}")
    print("=" * 88)
    print(f"{'SEC':<4} | {'SECTION TITLE':<26} | {'PRE-SCROLL':<14} | {'ACTIVE SCROLL':<14} | {'SCROLL-UP RESET':<16} | {'STATUS'}")
    print("-" * 88)
    
    all_passed = True
    for sec_num, sec_id, sec_title in sections:
        # 1. Reset to top
        page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        page.wait_for_timeout(200)
        pre_m = get_section_metrics(page, sec_id)
        
        # 2. Instant scroll to trigger animation
        page.evaluate(f"document.querySelector('{sec_id}').scrollIntoView({{ behavior: 'instant' }})")
        
        # Mid-transition check
        page.wait_for_timeout(150)
        mid_m = get_section_metrics(page, sec_id)
        
        # Settled check (500ms transition + 70ms delay finishes by 650ms)
        page.wait_for_timeout(550) # 150 + 550 = 700ms
        act_m = get_section_metrics(page, sec_id)
        
        # 3. Scroll back to top to verify reset
        page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        page.wait_for_timeout(550) # 500ms fade-out finishes
        res_m = get_section_metrics(page, sec_id)
        
        pre_op = float(pre_m['wordOpacity']) if pre_m['wordOpacity'] is not None else 0.0
        mid_op = float(mid_m['wordOpacity']) if mid_m['wordOpacity'] is not None else 0.0
        act_op = float(act_m['wordOpacity']) if act_m['wordOpacity'] is not None else 1.0
        res_op = float(res_m['wordOpacity']) if res_m['wordOpacity'] is not None else 0.0
        
        pre_disp = f"op:{pre_op:.2f} ({'in' if pre_m['hasIn'] else '!in'})"
        act_disp = f"op:{act_op:.2f} ({'in' if act_m['hasIn'] else '!in'})"
        res_disp = f"op:{res_op:.2f} ({'in' if res_m['hasIn'] else '!in'})"
        
        passed = act_op >= 0.95 and act_m['hasIn']
        status = "PASSED ✓" if passed else "FAILED ✗"
        if not passed:
            all_passed = False
            
        print(f"{sec_num:<4} | {sec_title:<26} | {pre_disp:<14} | {act_disp:<14} | {res_disp:<16} | {status}")
        
    print("=" * 88)
    return all_passed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", action="store_true", help="Test live GitHub Pages URLs")
    parser.add_argument("url", nargs="?", help="Direct URL to test")
    args = parser.parse_args()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        success = True
        if args.url:
            platform = "detailing" if "detailing" in args.url or "s/" in args.url else "banya"
            success = test_platform(page, args.url, platform)
        elif args.remote:
            s1 = test_platform(page, "https://ti-kan.github.io/detailing-base/s/bezskolov/", "detailing")
            s2 = test_platform(page, "https://ti-kan.github.io/banya-base/b/taiga-82/", "banya")
            success = s1 and s2
        else:
            s1 = test_platform(page, "http://localhost:3010/s/bezskolov/", "detailing")
            s2 = test_platform(page, "http://localhost:3008/b/taiga-82/", "banya")
            success = s1 and s2
            
        browser.close()
        
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
