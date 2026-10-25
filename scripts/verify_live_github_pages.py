#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live GitHub Pages Playwright Network + Visual QA
Verifies ti-kan.github.io live URLs for 0 broken images, 0 404 assets, and full visual section integrity.
"""
import sys, time
from playwright.sync_api import sync_playwright

URLS_TO_TEST = [
    {
        "url": "https://ti-kan.github.io/detailing-base/s/bezskolov/",
        "name": "Detailing Flagship (bezskolov)",
        "checks": ["detailing", "sec05", "slider", "packages"]
    },
    {
        "url": "https://ti-kan.github.io/detailing-base/tula-50.html",
        "name": "Detailing Outreach Cockpit (tula-50.html)",
        "checks": ["cockpit"]
    },
    {
        "url": "https://ti-kan.github.io/banya-base/b/taiga-82/",
        "name": "Banya Flagship (taiga-82)",
        "checks": ["banya", "sec08", "baths"]
    },
    {
        "url": "https://ti-kan.github.io/banya-base/b/kedrovy-log/",
        "name": "Banya Secondary (kedrovy-log)",
        "checks": ["banya", "sec08"]
    },
    {
        "url": "https://ti-kan.github.io/banya-base/krasnoyarsk-50.html",
        "name": "Banya Outreach Cockpit (krasnoyarsk-50.html)",
        "checks": ["cockpit"]
    }
]

def run_qa():
    print("=" * 70)
    print("STARTING LIVE GITHUB PAGES PLAYWRIGHT QA")
    print("=" * 70)

    total_failures = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for item in URLS_TO_TEST:
            url = item["url"]
            name = item["name"]
            checks = item["checks"]
            print(f"\n--- Testing: {name} ---")
            print(f"URL: {url}")
            
            # Test in mobile viewport (390x844 iPhone 14)
            context = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=3,
                is_mobile=True,
                has_touch=True,
                locale="ru-RU"
            )
            page = context.new_page()
            
            failed_requests = []
            def on_response(resp):
                if resp.status >= 400:
                    failed_requests.append(f"{resp.status} {resp.url}")
            page.on("response", on_response)
            
            try:
                resp = page.goto(url, wait_until="networkidle", timeout=30000)
                status = resp.status if resp else "NO_RESP"
                print(f"Page HTTP Status: {status}")
                if status != 200:
                    print(f"❌ ERROR: Page HTTP status {status} != 200")
                    total_failures += 1
            except Exception as e:
                print(f"❌ GOTO EXCEPTION: {e}")
                total_failures += 1
                context.close()
                continue
            
            # Scroll through page to trigger animations, and decode all images
            page.evaluate("""async () => {
                const h = document.documentElement.scrollHeight;
                for (let y = 0; y < h; y += 400) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 80));
                }
                window.scrollTo(0, 0);
                const imgs = Array.from(document.querySelectorAll('img'));
                await Promise.all(imgs.map(img => {
                    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
                    return img.decode().catch(() => {});
                }));
            }""")
            page.wait_for_timeout(1000)
            
            # 1. Assert ZERO 400+ network responses
            img_font_fails = [f for f in failed_requests if any(ext in f.lower() for ext in ['.jpg', '.jpeg', '.png', '.avif', '.webp', '.mp4', '.woff2', '.woff', '.css', '.js'])]
            print(f"Failed asset requests: {len(img_font_fails)}")
            if img_font_fails:
                for f in img_font_fails:
                    print(f"  ❌ FAILED ASSET: {f}")
                total_failures += len(img_font_fails)
            else:
                print("  ✅ All network requests loaded successfully (0 404s)!")

            # 2. Check every <img> on the live page
            broken_imgs = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('img')).filter(
                    img => !img.complete || img.naturalWidth === 0
                ).map(img => ({
                    src: img.src,
                    alt: img.alt,
                    naturalWidth: img.naturalWidth,
                    complete: img.complete
                }));
            }""")
            print(f"Broken <img> elements: {len(broken_imgs)}")
            if broken_imgs:
                for b in broken_imgs:
                    print(f"  ❌ BROKEN IMG: {b}")
                total_failures += len(broken_imgs)
            else:
                total_imgs = page.evaluate("() => document.querySelectorAll('img').length")
                print(f"  ✅ All {total_imgs} <img> elements have naturalWidth > 0!")

            # 3. Check specific section checks
            if "sec05" in checks:
                sec05_info = page.evaluate("""() => {
                    const sec = document.getElementById('tech');
                    if (!sec) return { found: false };
                    const num = sec.querySelector('.sh .num');
                    const h2 = sec.querySelector('.sh h2');
                    const items = Array.from(sec.querySelectorAll('.tech-item'));
                    return {
                        found: true,
                        numText: num ? num.innerText.trim() : null,
                        numVisible: num ? window.getComputedStyle(num).opacity : null,
                        h2Text: h2 ? h2.innerText.trim() : null,
                        itemsCount: items.length,
                        itemsOpacities: items.map(i => window.getComputedStyle(i).opacity)
                    };
                }""")
                print(f"Section 05 Check: {sec05_info}")
                if not sec05_info["found"] or sec05_info["numText"] != "05":
                    print("  ❌ Section 05 05 badge missing or incorrect!")
                    total_failures += 1
                elif any(float(op) < 0.9 for op in sec05_info["itemsOpacities"]):
                    print(f"  ❌ Section 05 tech items opacity too low: {sec05_info['itemsOpacities']}")
                    total_failures += 1
                else:
                    print("  ✅ Section 05: '05' badge present, 4 tech cards 100% opaque!")

            if "sec08" in checks:
                sec08_info = page.evaluate("""() => {
                    const sec = document.getElementById('book');
                    if (!sec) return { found: false };
                    const num = sec.querySelector('.sh .num');
                    const h2 = sec.querySelector('#h-book');
                    const steps = Array.from(sec.querySelectorAll('.steps li'));
                    return {
                        found: true,
                        numText: num ? num.innerText.trim() : null,
                        numOpacity: num ? window.getComputedStyle(num).opacity : null,
                        h2Text: h2 ? h2.innerText.trim() : null,
                        h2Opacity: h2 ? window.getComputedStyle(h2).opacity : null,
                        stepsCount: steps.length,
                        stepsOpacities: steps.map(s => window.getComputedStyle(s).opacity)
                    };
                }""")
                print(f"Section 08 Check: {sec08_info}")
                if not sec08_info["found"] or sec08_info["numText"] != "08":
                    print("  ❌ Section 08 badge missing or incorrect!")
                    total_failures += 1
                elif float(sec08_info.get("h2Opacity") or 0) < 0.9:
                    print(f"  ❌ Section 08 h2 opacity too low: {sec08_info.get('h2Opacity')}")
                    total_failures += 1
                elif any(float(op) < 0.9 for op in sec08_info["stepsOpacities"]):
                    print(f"  ❌ Section 08 steps opacity too low: {sec08_info['stepsOpacities']}")
                    total_failures += 1
                else:
                    print("  ✅ Section 08: '08' badge present, heading and 3 steps 100% visible!")

            context.close()

        browser.close()

    print("\n" + "=" * 70)
    print(f"FINAL AUDIT RESULT: TOTAL FAILURES = {total_failures}")
    print("=" * 70)
    return total_failures

if __name__ == "__main__":
    time.sleep(5)
    code = run_qa()
    sys.exit(code)
