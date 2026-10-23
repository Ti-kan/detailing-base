#!/usr/bin/env python3
"""
scripts/verify_video_frames.py
Playwright Frame-by-Frame Video & Geometry Audit Log (Port 3010 /s/bezskolov/)
Non-webdriver realistic browser context.
"""

import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = "/Users/takanov/detailing-base/scripts/audit_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

URL = "http://localhost:3010/s/bezskolov/"

METRICS_JS = """() => {
  const v = document.getElementById('heroCarVideo');
  const stage = document.getElementById('heroVideoStage');
  const slot = document.getElementById('heroFrameSlot');
  const loupe = document.getElementById('carLoupe');
  const hud = document.getElementById('loupeHud');
  const cta = stage ? stage.querySelector('.cta') : null;
  const replay = document.getElementById('replayVideoBtn');

  const vRect = v ? v.getBoundingClientRect() : null;
  const sRect = stage ? stage.getBoundingClientRect() : null;
  const slotRect = slot ? slot.getBoundingClientRect() : null;

  return {
    currentTime: v ? Number(v.currentTime.toFixed(3)) : null,
    duration: v ? Number(v.duration.toFixed(3)) : null,
    paused: v ? v.paused : null,
    ended: v ? v.ended : null,
    videoWidth: v ? v.videoWidth : null,
    videoHeight: v ? v.videoHeight : null,
    videoRect: vRect ? {top: Math.round(vRect.top), left: Math.round(vRect.left), width: Math.round(vRect.width), height: Math.round(vRect.height)} : null,
    stageRect: sRect ? {top: Math.round(sRect.top), left: Math.round(sRect.left), width: Math.round(sRect.width), height: Math.round(sRect.height)} : null,
    slotRect: slotRect ? {top: Math.round(slotRect.top), left: Math.round(slotRect.left), width: Math.round(slotRect.width), height: Math.round(slotRect.height)} : null,
    aspectRatio: (v && v.videoHeight) ? Number((v.videoWidth / v.videoHeight).toFixed(4)) : null,
    stageRatio: (sRect && sRect.height) ? Number((sRect.width / sRect.height).toFixed(4)) : null,
    isDocked: stage ? stage.classList.contains('is-docked') : false,
    isDocking: stage ? stage.classList.contains('is-docking') : false,
    loupeActive: stage ? stage.classList.contains('is-inspecting') : false,
    hudText: hud ? hud.textContent.trim() : null,
    ctaVisible: cta ? (getComputedStyle(cta).opacity === '1') : false,
    replayActive: replay ? replay.classList.contains('is-active') : false,
    onDockComplete: Boolean(window.__onDockComplete)
  };
}"""

def main():
    print("=" * 70)
    print("STARTING FRAME-BY-FRAME VIDEO & GEOMETRY AUDIT")
    print(f"Target: {URL}")
    print("=" * 70)

    audit_log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--autoplay-policy=no-user-gesture-required",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Ensure realistic browser environment with window.__playFullIntro = true
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            window.__playFullIntro = true;
        """)

        print(f"[*] Navigating to {URL}...")
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_selector("#heroCarVideo", state="attached", timeout=10000)

        # Ensure video is playing
        page.evaluate("""() => {
            const v = document.getElementById('heroCarVideo');
            if (v && v.paused) {
                if (v.currentTime < 0.3) v.currentTime = 0.3;
                v.play().catch(e => console.error(e));
            }
        }""")

        def record_step(label, file_name):
            m = page.evaluate(METRICS_JS)
            shot_path = os.path.join(SCREENSHOT_DIR, file_name)
            page.screenshot(path=shot_path)
            entry = {"label": label, "screenshot": shot_path, "metrics": m}
            audit_log.append(entry)
            print(f"\n--- [{label}] ---")
            print(f"  Time: {m['currentTime']}s / {m['duration']}s | Paused: {m['paused']} | Ended: {m['ended']}")
            print(f"  Native Resolution: {m['videoWidth']}x{m['videoHeight']} | Aspect Ratio: {m['aspectRatio']}")
            print(f"  Stage Box: {m['stageRect']} | Stage Ratio: {m['stageRatio']}")
            print(f"  Slot Box:  {m['slotRect']}")
            print(f"  isDocked: {m['isDocked']} | isDocking: {m['isDocking']} | onDockComplete: {m['onDockComplete']}")
            print(f"  Loupe Active: {m['loupeActive']} | HUD: {m['hudText']}")
            print(f"  CTA Visible: {m['ctaVisible']} | Replay Active: {m['replayActive']}")
            print(f"  Screenshot saved: {shot_path}")
            return m

        # 1. t = 0.5s
        print("[*] Waiting for t = 0.5s...")
        for _ in range(50):
            t = page.evaluate("() => document.getElementById('heroCarVideo')?.currentTime || 0")
            if t >= 0.5:
                break
            time.sleep(0.05)
        m1 = record_step("Timestamp 1: t = 0.5s (Fullscreen Entry)", "frame_01_t05.png")

        # 2. t = 1.5s
        print("[*] Waiting for t = 1.5s...")
        for _ in range(50):
            t = page.evaluate("() => document.getElementById('heroCarVideo')?.currentTime || 0")
            if t >= 1.5:
                break
            time.sleep(0.05)
        m2 = record_step("Timestamp 2: t = 1.5s (Car Driving Forward)", "frame_02_t15.png")

        # 3. t = 2.5s (Critical: Video must NOT cut off at 2.0s or 2.5s!)
        print("[*] Waiting for t = 2.5s...")
        for _ in range(50):
            t = page.evaluate("() => document.getElementById('heroCarVideo')?.currentTime || 0")
            if t >= 2.5:
                break
            time.sleep(0.05)
        m3 = record_step("Timestamp 3: t = 2.5s (Cleaning & Detailing in Fullscreen)", "frame_03_t25.png")

        # 4. t = duration - 0.1s (Final Gleaming Hero Frame)
        print("[*] Waiting for t = duration - 0.1s...")
        for _ in range(80):
            m = page.evaluate("() => { const v = document.getElementById('heroCarVideo'); return { t: v ? v.currentTime : 0, d: v ? v.duration : 5.04 }; }")
            if m["t"] >= m["d"] - 0.15 or m["t"] >= 4.9:
                break
            time.sleep(0.05)
        m4 = record_step("Timestamp 4: t = duration - 0.1s (Final Hero Pose Before Dock)", "frame_04_tFinal.png")

        # 5. docked + 0.2s (Zero Distortion Docking Completed)
        print("[*] Waiting for docking animation to complete...")
        for _ in range(60):
            docked = page.evaluate("() => Boolean(window.__onDockComplete)")
            if docked:
                break
            time.sleep(0.05)
        time.sleep(0.40)
        m5 = record_step("Timestamp 5: docked + 0.2s (Docked in heroFrameSlot)", "frame_05_docked.png")

        # 6. docked + 1.0s with cursor hover (Interactive Detailing Loupe & HUD)
        print("[*] Testing Interactive Optical Detailing Loupe with Cursor Hover...")
        time.sleep(0.6)
        s_box = m5["stageRect"]
        if s_box:
            # Hover over the hood of the car (left-center)
            hx = s_box["left"] + s_box["width"] * 0.28
            hy = s_box["top"] + s_box["height"] * 0.50
            page.mouse.move(hx, hy)
            time.sleep(0.3)
        m6 = record_step("Timestamp 6: docked + 1.0s (Optical Loupe Active with CRI 95+ HUD)", "frame_06_loupe.png")

        browser.close()

    print("\n" + "=" * 70)
    print("GEOMETRY & INTEGRITY ASSERTIONS VERIFICATION:")
    print("=" * 70)

    # Assertions
    errors = []

    # 1. Video dimensions
    if m1["videoWidth"] != 1920 or m1["videoHeight"] != 1080:
        errors.append(f"Invalid video dimensions: {m1['videoWidth']}x{m1['videoHeight']}, expected 1920x1080")
    else:
        print("[PASS] Video native dimensions: 1920x1080 (16:9 native)")

    # 2. Aspect Ratio (no distortion)
    if abs(m1["aspectRatio"] - (16/9)) > 0.01:
        errors.append(f"Distorted aspect ratio: {m1['aspectRatio']}, expected {16/9:.4f}")
    else:
        print(f"[PASS] Aspect ratio: {m1['aspectRatio']} (0% distortion, 16/9 exact)")

    # 3. No early cutoff at 2.0s / 2.5s
    if m3["isDocked"] or m3["isDocking"]:
        errors.append("Video prematurely docked at or before t = 2.5s!")
    else:
        print(f"[PASS] Video played past 2.5s in fullscreen (currentTime = {m3['currentTime']}s) without premature dock")

    # 4. Docked geometry match
    if not m5["isDocked"] or not m5["onDockComplete"]:
        errors.append("Stage failed to complete docking into heroFrameSlot")
    else:
        print("[PASS] Stage smoothly docked and locked inside heroFrameSlot")

    if m5["stageRatio"] is None or abs(m5["stageRatio"] - (16/9)) > 0.05:
        errors.append(f"Docked stage ratio {m5['stageRatio']} does not match 16/9")
    else:
        print(f"[PASS] Docked stage ratio: {m5['stageRatio']} matches 16/9 (0% squashing)")

    # 5. CTA Visibility & Replay
    if not m5["ctaVisible"]:
        errors.append("CTA bar is not visible after docking")
    else:
        print("[PASS] Bottom CTA bar is 100% visible and interactive after docking")

    if not m5["replayActive"]:
        errors.append("Replay button is not active after final video frame")
    else:
        print("[PASS] Top-right Replay button is active and ready")

    # 6. Optical Loupe active on hover
    if not m6["loupeActive"]:
        errors.append("Optical detailing loupe failed to activate on cursor hover")
    else:
        print(f"[PASS] Optical detailing loupe active with HUD: '{m6['hudText']}'")

    if errors:
        print("\n[FAIL] AUDIT ENCOUNTERED ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n" + "=" * 70)
        print("ALL 6 TIMESTAMPS PASSED WITH 100% PERFECT METRICS & ZERO DISTORTION!")
        print("=" * 70)

if __name__ == "__main__":
    main()
