import sys
import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        print("Launching stealth browser...")
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai"
        )
        # Anti-detection stealth script
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)
        
        page = context.new_page()
        
        url = "https://permit.mee.gov.cn/permitExt/defaults/default-index!getInformation.action"
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)
        
        print("Page title:", page.title())
        
        # Click on "许可信息公开" (Tab 2 or link)
        print("Clicking 许可信息公开...")
        page.click("text=许可信息公开")
        page.wait_for_timeout(3000)
        
        print("Current page URL:", page.url)
        
        # Select province "吉林省" (value 220000000000)
        print("Selecting 吉林省...")
        page.select_option("#province", value="220000000000")
        page.wait_for_timeout(2000)
        
        # Click Search button
        print("Clicking search...")
        page.click("input.search-btn, input[onclick='query()'], button:has-text('搜索')")
        page.wait_for_timeout(4000)
        
        # Extract rows
        rows_count = page.evaluate("() => document.querySelectorAll('table tr').length - 1")
        print(f"Found {rows_count} enterprise rows on Page 1!")
        
        first_company = page.evaluate("""() => {
            const rows = document.querySelectorAll('table tr');
            if (rows.length > 1) {
                return rows[1].innerText.replace(/\\s+/g, ' ');
            }
            return 'NONE';
        }""")
        print(f"First company snippet: {first_company}")
        
        browser.close()

if __name__ == '__main__':
    run_test()
