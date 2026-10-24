#!/usr/bin/env python3
"""
Full QA verification suite for:
- 96px compact jewel lens (no crosshair, no colliding badge, single lightning icon)
- In-frame video replay
- Section headers 01 to 08 with 3D number tags
- Mobile responsiveness (390x844) on detailing and banya
"""
import sys
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = "/Users/takanov/.gemini/antigravity-cli/brain/0cba8e2f-79d3-4c29-a34a-d0fa28861163"

def run_qa():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        # ----------------------------------------------------
        # 1. Desktop Detailing (1440x900): 96px lens hover test
        # ----------------------------------------------------
        print("1. Testing 96px lens hover on Desktop (1440x900)...")
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
            has_touch=False
        )
        page = ctx.new_page()
        page.goto("http://localhost:3010/s/bezskolov/", wait_until="networkidle")

        # Ensure docked
        page.evaluate("""() => {
            if (window.__dockVideo) window.__dockVideo();
            const stage = document.getElementById('heroVideoStage');
            if (stage) stage.classList.add('is-docked');
            window.__onDockComplete = true;
        }""")
        page.wait_for_timeout(1000)

        # Move mouse to center of hood (left ~32%, top ~52% of .frame)
        frame_box = page.locator("#heroFrameSlot").bounding_box()
        if frame_box:
            hover_x = frame_box["x"] + frame_box["width"] * 0.32
            hover_y = frame_box["y"] + frame_box["height"] * 0.52
            page.mouse.move(hover_x, hover_y)
            page.wait_for_timeout(400)

        page.screenshot(path=f"{ARTIFACT_DIR}/qa_1_detailing_96px_lens.png", clip={
            "x": 0, "y": 0, "width": 1440, "height": 850
        })
        print(f"Captured {ARTIFACT_DIR}/qa_1_detailing_96px_lens.png")

        # ----------------------------------------------------
        # 2. In-Frame Video Replay Test
        # ----------------------------------------------------
        print("2. Testing In-Frame Replay...")
        replay_btn = page.locator("#replayVideoBtn")
        replay_btn.click()
        page.wait_for_timeout(600)

        # Check replay state
        is_replaying = page.evaluate("""() => {
            const stage = document.getElementById('heroVideoStage');
            const vid = document.getElementById('heroCarVideo');
            const btn = document.getElementById('replayVideoBtn');
            return {
                stageHasClass: stage.classList.contains('is-replaying'),
                videoPaused: vid.paused,
                videoZIndex: window.getComputedStyle(vid).zIndex,
                btnText: btn.innerText.trim(),
                currentTime: vid.currentTime
            };
        }""")
        print("Replay state after click:", is_replaying)
        assert is_replaying["stageHasClass"], "Stage should have .is-replaying class"
        assert "Идёт заезд" in is_replaying["btnText"], "Button should show 'Идёт заезд'"

        # Capture in-frame replay in action
        page.screenshot(path=f"{ARTIFACT_DIR}/qa_2_detailing_inframe_replay.png", clip={
            "x": 0, "y": 0, "width": 1440, "height": 750
        })
        print(f"Captured {ARTIFACT_DIR}/qa_2_detailing_inframe_replay.png")

        # Wait for replay to complete or fast forward
        page.evaluate("""() => {
            const vid = document.getElementById('heroCarVideo');
            if (vid) {
                vid.currentTime = vid.duration - 0.05;
            }
        }""")
        page.wait_for_timeout(500)

        after_replay = page.evaluate("""() => {
            const stage = document.getElementById('heroVideoStage');
            const btn = document.getElementById('replayVideoBtn');
            return {
                stageHasClass: stage.classList.contains('is-replaying'),
                btnText: btn.innerText.trim()
            };
        }""")
        print("State after video ended:", after_replay)
        assert not after_replay["stageHasClass"], "Stage should NOT have .is-replaying after completion"

        # ----------------------------------------------------
        # 3. Section Headers 01 to 08
        # ----------------------------------------------------
        print("3. Testing Section Headers 01 to 08...")
        page.evaluate("""() => {
            document.querySelectorAll('.sh, .reveal').forEach(el => {
                el.classList.add('on');
                el.classList.add('in');
            });
        }""")
        page.wait_for_timeout(500)
        page.screenshot(path=f"{ARTIFACT_DIR}/qa_3_detailing_headers_01_to_08.png", full_page=True)
        print(f"Captured {ARTIFACT_DIR}/qa_3_detailing_headers_01_to_08.png")
        ctx.close()

        # ----------------------------------------------------
        # 4. Mobile Detailing (390x844 iPhone 14)
        # ----------------------------------------------------
        print("4. Testing Mobile Detailing (390x844)...")
        m_ctx = browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
            has_touch=True,
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        m_page = m_ctx.new_page()
        m_page.goto("http://localhost:3010/s/bezskolov/", wait_until="networkidle")
        m_page.evaluate("""() => {
            if (window.__dockVideo) window.__dockVideo();
            const stage = document.getElementById('heroVideoStage');
            if (stage) stage.classList.add('is-docked');
            window.__onDockComplete = true;
            document.querySelectorAll('.sh, .reveal').forEach(el => {
                el.classList.add('on');
                el.classList.add('in');
            });
        }""")
        m_page.wait_for_timeout(600)

        # Trigger mobile touch wiper on hood
        m_frame = m_page.locator("#heroFrameSlot").bounding_box()
        if m_frame:
            tx = m_frame["x"] + m_frame["width"] * 0.35
            ty = m_frame["y"] + m_frame["height"] * 0.5
            m_page.touchscreen.tap(tx, ty)
            m_page.wait_for_timeout(300)

        m_page.screenshot(path=f"{ARTIFACT_DIR}/qa_4_mobile_detailing_390.png", full_page=True)
        print(f"Captured {ARTIFACT_DIR}/qa_4_mobile_detailing_390.png")
        m_ctx.close()

        # ----------------------------------------------------
        # 5. Mobile Banya (390x844 iPhone 14)
        # ----------------------------------------------------
        print("5. Testing Mobile Banya (390x844)...")
        b_ctx = browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
            has_touch=True,
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        b_page = b_ctx.new_page()
        b_page.goto("http://localhost:3008/b/taiga-82/", wait_until="networkidle")
        b_page.evaluate("""() => {
            document.querySelectorAll('.sh, .reveal').forEach(el => {
                el.classList.add('on');
                el.classList.add('in');
            });
        }""")
        b_page.wait_for_timeout(600)
        b_page.screenshot(path=f"{ARTIFACT_DIR}/qa_5_mobile_banya_390.png", full_page=True)
        print(f"Captured {ARTIFACT_DIR}/qa_5_mobile_banya_390.png")
        b_ctx.close()

        browser.close()
        print("ALL QA SCREENSHOTS CAPTURED SUCCESSFULLY!")

if __name__ == "__main__":
    run_qa()
