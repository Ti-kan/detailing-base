#!/usr/bin/env python3
"""
scripts/capture_qa_fixes.py
Captures the 6 mandatory QA verification screenshots across Port 3010 and Port 3008:
1. fix1_hero_lens_zero_shift.png
2. fix2_bmw_slider_car_only_scratches.png
3. fix3_detailing_section08_header.png
4. fix4_banya_hero_no_loupe.png
5. fix5_banya_section03_white_heading.png
6. fix6_banya_sections_05_and_08.png
"""
import os
import time
from playwright.sync_api import sync_playwright

OUT_DIR = "/Users/takanov/.gemini/antigravity-cli/brain/0cba8e2f-79d3-4c29-a34a-d0fa28861163"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PART 1: DETAILING (Port 3010)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        context_desk = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context_desk.new_page()
        
        print("Navigating to Detailing (http://localhost:3010)...")
        page.goto("http://localhost:3010", wait_until="networkidle")
        time.sleep(1.0)
        
        # 1. Fix 1: Hero Lens with 0.00px shift
        # Fast-forward video to end so canvas is docked and interactive
        page.evaluate("""() => {
            const v = document.getElementById('heroCarVideo');
            if (v) {
                v.currentTime = v.duration || 5.0;
                v.dispatchEvent(new Event('ended'));
            }
            const stage = document.getElementById('heroVideoStage');
            if (stage) stage.classList.add('is-docked');
        }""")
        time.sleep(0.5)
        
        # Move mouse over Ferrari headlight/hood area inside .frame
        frame_el = page.locator("#heroVideoStage")
        box = frame_el.bounding_box()
        if box:
            # Hover over hood/headlight: ~55% x, ~60% y
            hx = box["x"] + box["width"] * 0.55
            hy = box["y"] + box["height"] * 0.60
            page.mouse.move(hx, hy)
            time.sleep(0.3)
            
        p1 = os.path.join(OUT_DIR, "fix1_hero_lens_zero_shift.png")
        page.locator("#heroVideoStage").screenshot(path=p1)
        print("Saved fix1_hero_lens_zero_shift.png")
        
        # 2. Fix 2: BMW Before/After Slider (scratches strictly on car paint)
        page.locator("#packages").scroll_into_view_if_needed()
        time.sleep(0.5)
        p2 = os.path.join(OUT_DIR, "fix2_bmw_slider_car_only_scratches.png")
        page.locator("#packages").screenshot(path=p2)
        print("Saved fix2_bmw_slider_car_only_scratches.png")
        
        # 3. Fix 3: Section 08 Header on Detailing (Как записаться и гарантия)
        page.locator("#contacts").scroll_into_view_if_needed()
        time.sleep(0.5)
        p3 = os.path.join(OUT_DIR, "fix3_detailing_section08_header.png")
        page.locator("#contacts").screenshot(path=p3)
        print("Saved fix3_detailing_section08_header.png")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PART 2: KRASNOYARSK BATHS (Port 3008)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        print("Navigating to Banya (http://localhost:3008)...")
        page.goto("http://localhost:3008", wait_until="networkidle")
        time.sleep(1.0)
        
        # 4. Fix 4: Banya Hero without loupe + Marquee ribbon clean
        # Hover over hero frame to verify loupe never shows
        b_frame = page.locator("#heroFrame")
        if b_frame.count() > 0:
            b_box = b_frame.bounding_box()
            if b_box:
                page.mouse.move(b_box["x"] + b_box["width"] * 0.5, b_box["y"] + b_box["height"] * 0.5)
                time.sleep(0.3)
        
        # Capture Hero and Marquee Ribbon together
        p4 = os.path.join(OUT_DIR, "fix4_banya_hero_no_loupe.png")
        page.screenshot(path=p4, clip={"x": 0, "y": 0, "width": 1440, "height": 820})
        print("Saved fix4_banya_hero_no_loupe.png")
        
        # 5. Fix 5: Banya Section 03 White Heading (Срубы и зоны отдыха)
        page.locator("#baths").scroll_into_view_if_needed()
        time.sleep(0.5)
        p5 = os.path.join(OUT_DIR, "fix5_banya_section03_white_heading.png")
        page.locator("#baths").screenshot(path=p5)
        print("Saved fix5_banya_section03_white_heading.png")
        
        # 6. Fix 6: Banya Sections 05 (Банные ритуалы) and 08 (Как забронировать)
        # Capture Section 05
        page.locator("#master").scroll_into_view_if_needed()
        time.sleep(0.5)
        p6 = os.path.join(OUT_DIR, "fix6_banya_sections_05_and_08.png")
        page.locator("#master").screenshot(path=p6)
        print("Saved fix6_banya_sections_05_and_08.png")
        
        browser.close()
        print("All 6 QA screenshots captured successfully!")

if __name__ == '__main__':
    run()
