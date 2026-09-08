import os
import sys
import time
import json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"d:\Tools of Jawad\24- Data Analysis\UI Structure"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def capture_full_height(page, path):
    # Find total block height
    block_h = page.evaluate("""() => {
        const el = document.querySelector('.block-container') || document.querySelector('.stApp');
        return el ? Math.max(el.scrollHeight, document.documentElement.scrollHeight, 1080) : 1080;
    }""")
    current_size = page.viewport_size
    page.set_viewport_size({"width": 1920, "height": block_h + 100})
    page.wait_for_timeout(600)
    page.screenshot(path=path)
    # Reset viewport back to 1080
    page.set_viewport_size(current_size)
    page.wait_for_timeout(300)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page = context.new_page()

        print("Navigating to Executive Cockpit (http://localhost:8501/)...")
        page.goto("http://localhost:8501/", wait_until="networkidle")
        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # PART 1: EXECUTIVE COCKPIT TABS
        # -------------------------------------------------------------
        print("=== PART 1: EXECUTIVE COCKPIT ===")
        
        # 01. PowerBI Studio - Top Viewport
        print("Capturing 01_Executive_Cockpit_PowerBI_Studio_Top.png...")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_Executive_Cockpit_PowerBI_Studio_Top.png"))

        # 02. PowerBI Studio - Mid (Charts & Waterfall)
        print("Capturing 02_Executive_Cockpit_PowerBI_Studio_Charts.png...")
        page.evaluate("window.scrollTo(0, 750)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_Executive_Cockpit_PowerBI_Studio_Charts.png"))

        # 03. PowerBI Studio - Bottom (MoM Table)
        print("Capturing 03_Executive_Cockpit_PowerBI_Studio_Table.png...")
        page.evaluate("window.scrollTo(0, 1600)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_Executive_Cockpit_PowerBI_Studio_Table.png"))

        # PowerBI Full Height Page
        print("Capturing 01b_Executive_Cockpit_PowerBI_Studio_FullPage.png...")
        capture_full_height(page, os.path.join(OUTPUT_DIR, "01b_Executive_Cockpit_PowerBI_Studio_FullPage.png"))

        # Retrieve tabs using modern Streamlit selector
        page.evaluate("window.scrollTo(0, 380)")
        page.wait_for_timeout(500)
        tabs = page.query_selector_all('div[data-testid="stTab"]')
        print(f"Detected {len(tabs)} tabs in Executive Cockpit.")

        exec_tabs_info = [
            (1, "04_Executive_Cockpit_Agentic_Workflow", "6-Step Agentic Workflow"),
            (2, "05_Executive_Cockpit_Portfolio_Matrix", "5-Product Portfolio Matrix"),
            (3, "06_Executive_Cockpit_Diagnostic_Engine", "Dynamic Diagnostic Engine"),
            (4, "07_Executive_Cockpit_Live_Simulator", "Live Action Simulator"),
            (5, "08_Executive_Cockpit_BiWeekly_Report", "Bi-Weekly Intelligence Report"),
            (6, "09_Executive_Cockpit_GCCO_Briefing", "GCCO Escalation Briefing")
        ]

        for idx, file_prefix, label in exec_tabs_info:
            if idx < len(tabs):
                print(f"Clicking Tab [{idx}]: {label}...")
                tabs[idx].click()
                page.wait_for_timeout(2500)
                page.evaluate("window.scrollTo(0, 380)")
                page.wait_for_timeout(800)
                
                # Standard 1080 Viewport capture
                vp_file = os.path.join(OUTPUT_DIR, f"{file_prefix}_Viewport.png")
                page.screenshot(path=vp_file)
                print(f"Saved Viewport: {vp_file}")

                # Complete full height page capture
                fp_file = os.path.join(OUTPUT_DIR, f"{file_prefix}_FullPage.png")
                capture_full_height(page, fp_file)
                print(f"Saved Full Height: {fp_file}")

        # -------------------------------------------------------------
        # PART 2: JD COPILOT CHAT EXPERIENCE
        # -------------------------------------------------------------
        print("\n=== PART 2: JD COPILOT CHAT EXPERIENCE ===")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(800)
        popover_btn = page.query_selector('div[data-testid="stPopover"] button, button[data-testid="stPopoverButton"]')
        if popover_btn:
            popover_btn.click()
            page.wait_for_timeout(1500)
            chat_file = os.path.join(OUTPUT_DIR, "10_Executive_Cockpit_JD_Copilot_Chat_Open.png")
            page.screenshot(path=chat_file)
            print(f"Saved: {chat_file}")

            # Close popover
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # PART 3: FRONTLINE KNOWLEDGE ASSISTANT (INITIATIVE 1)
        # -------------------------------------------------------------
        print("\n=== PART 3: FRONTLINE KNOWLEDGE ASSISTANT ===")
        radios = page.query_selector_all('div[data-testid="stRadio"] label')
        frontline_radio = None
        for r in radios:
            if "Frontline Knowledge Assistant" in (r.inner_text() or ""):
                frontline_radio = r
                break

        if frontline_radio:
            print("Switching to Frontline Knowledge Assistant...")
            frontline_radio.click()
            page.wait_for_timeout(3500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)

            # Tab 0: Ask Product Assistant
            fl_vp_0 = os.path.join(OUTPUT_DIR, "11_Frontline_Portal_Ask_Assistant_Viewport.png")
            fl_fp_0 = os.path.join(OUTPUT_DIR, "11_Frontline_Portal_Ask_Assistant_FullPage.png")
            page.screenshot(path=fl_vp_0)
            capture_full_height(page, fl_fp_0)
            print(f"Saved: {fl_vp_0} and {fl_fp_0}")

            # Click a scenario button to see grounded answer & fatwa citations
            scenario_btns = page.query_selector_all('button')
            for sb in scenario_btns:
                stext = sb.inner_text() or ""
                if "Booster Plan Milestone Bonus" in stext:
                    print(f"Clicking frontline scenario: '{stext}'...")
                    sb.click()
                    page.wait_for_timeout(4500)
                    page.evaluate("window.scrollTo(0, 450)")
                    page.wait_for_timeout(1000)
                    ans_file = os.path.join(OUTPUT_DIR, "11b_Frontline_Portal_Answer_Grounded_View.png")
                    ans_fp = os.path.join(OUTPUT_DIR, "11b_Frontline_Portal_Answer_Grounded_FullPage.png")
                    page.screenshot(path=ans_file)
                    capture_full_height(page, ans_fp)
                    print(f"Saved Grounded Answer: {ans_file} and {ans_fp}")
                    break

            # Now find Frontline tabs
            fl_tabs = page.query_selector_all('div[data-testid="stTab"]')
            print(f"Detected {len(fl_tabs)} tabs in Frontline Portal.")

            fl_tabs_info = [
                (1, "12_Frontline_Portal_Document_Inventory", "Approved Document Inventory (Phase 1A)"),
                (2, "13_Frontline_Portal_Escalations_Queue", "Escalation Management Queue (Phase 1B)"),
                (3, "14_Frontline_Portal_Compliance_Audit", "Compliance & InfoSec Audit Trail")
            ]

            for idx, file_prefix, label in fl_tabs_info:
                if idx < len(fl_tabs):
                    print(f"Clicking Frontline Tab [{idx}]: {label}...")
                    fl_tabs[idx].click()
                    page.wait_for_timeout(2500)
                    page.evaluate("window.scrollTo(0, 300)")
                    page.wait_for_timeout(800)

                    vp_file = os.path.join(OUTPUT_DIR, f"{file_prefix}_Viewport.png")
                    fp_file = os.path.join(OUTPUT_DIR, f"{file_prefix}_FullPage.png")
                    page.screenshot(path=vp_file)
                    capture_full_height(page, fp_file)
                    print(f"Saved: {vp_file} and {fp_file}")

        # -------------------------------------------------------------
        # PART 4: RESPONSIVE VIEWPORTS
        # -------------------------------------------------------------
        print("\n=== PART 4: RESPONSIVE BREAKPOINTS ===")
        # Tablet
        print("Capturing 15_Tablet_Responsive_768x1024.png...")
        t_ctx = browser.new_context(viewport={"width": 768, "height": 1024})
        t_page = t_ctx.new_page()
        t_page.goto("http://localhost:8501/", wait_until="networkidle")
        t_page.wait_for_timeout(3000)
        t_page.screenshot(path=os.path.join(OUTPUT_DIR, "15_Tablet_Responsive_768x1024.png"))
        capture_full_height(t_page, os.path.join(OUTPUT_DIR, "15b_Tablet_Responsive_FullPage.png"))
        t_ctx.close()

        # Mobile
        print("Capturing 16_Mobile_Responsive_390x844.png...")
        m_ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        m_page = m_ctx.new_page()
        m_page.goto("http://localhost:8501/", wait_until="networkidle")
        m_page.wait_for_timeout(3000)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "16_Mobile_Responsive_390x844.png"))
        capture_full_height(m_page, os.path.join(OUTPUT_DIR, "16b_Mobile_Responsive_FullPage.png"))
        m_ctx.close()

        browser.close()
        print("\nALL SCREENSHOTS CAPTURED WITH FULL HEIGHT RESOLUTION!")

if __name__ == "__main__":
    run()
