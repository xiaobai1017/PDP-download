import sys
import os
import re
import time
import csv
import random
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = 'https://permit.mee.gov.cn'
LICENSE_URL = f'{BASE_URL}/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action'

OUTPUT_DIR = r'c:\Users\hubin\workspace\PDP-download\pdf_downloads'
MANIFEST_CSV = r'c:\Users\hubin\workspace\PDP-download\downloads_manifest.csv'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

def sanitize_filename(filename):
    """Remove invalid Windows filename characters"""
    return re.sub(r'[\ \/\:\*\?\"\,\<\>\|]', '_', filename).strip()

def random_wait(min_s=1.5, max_s=3.5):
    """Human-like randomized sleep delay"""
    time.sleep(random.uniform(min_s, max_s))

class StealthPermitDownloader:
    def __init__(self, headless=True, start_page=1, max_pages=5):
        self.headless = headless
        self.start_page = start_page
        self.max_pages = max_pages
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def run(self):
        print("==================================================")
        print(f"Starting Stealth PDP Downloader (Pages: {self.start_page} to {self.max_pages})")
        print(f"Headless mode: {self.headless}")
        print("==================================================")

        with sync_playwright() as p:
            # Launch Chromium with anti-bot evasion arguments
            browser = p.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-infobars',
                    '--window-size=1920,1080'
                ]
            )

            context = browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={'width': 1920, 'height': 1080},
                locale="zh-CN",
                timezone_id="Asia/Shanghai"
            )

            # Anti-bot detection script injection
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            """)

            page = context.new_page()

            # Initialize CSV Manifest
            file_exists = os.path.exists(MANIFEST_CSV)
            csv_file = open(MANIFEST_CSV, 'a', newline='', encoding='utf-8-sig')
            fieldnames = [
                'page', 'index', 'province', 'city', 'xkz_num', 'company_name',
                'industry', 'valid_period', 'publish_date', 'mgmt_type',
                'pdf_filename', 'file_size', 'status', 'detail_url', 'download_url'
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            total_downloaded = 0
            total_failed = 0

            try:
                # Step 1: Open License Information Page Directly
                print(f"[Stealth] Navigating directly to license info page: {LICENSE_URL}")
                page.goto(LICENSE_URL, wait_until="networkidle", timeout=45000)
                random_wait(2, 4)

                # Step 2: Select Province = 吉林省 (220000000000)
                print("[Stealth] Selecting Province = 吉林省 (220000000000)...")
                page.select_option("#province", value="220000000000")
                random_wait(1, 2)

                # Step 3: Click Search Button
                print("[Stealth] Submitting search query...")
                page.click("input.search-btn, input[onclick='query()']")
                page.wait_for_load_state("networkidle")
                random_wait(3, 4)

                # Navigate / Jump to start_page if start_page > 1
                if self.start_page > 1:
                    print(f"[Stealth] Fast-forwarding to page {self.start_page}...")
                    page.evaluate(f"() => {{ jumpPage2({self.start_page}); }}")
                    page.wait_for_load_state("networkidle")
                    random_wait(3, 5)

                # Loop through target pages
                current_p = self.start_page
                while current_p <= self.max_pages:
                    print(f"\n--- Processing Page {current_p}/{self.max_pages} ---")

                    # Extract table data on current page
                    items = page.evaluate("""() => {
                        const table = document.querySelector('table');
                        if (!table) return [];
                        const rows = Array.from(table.querySelectorAll('tr')).slice(1);
                        return rows.map(r => {
                            const tds = r.querySelectorAll('td');
                            if (tds.length < 8) return null;
                            const a = r.querySelector('a');
                            const detailHref = a ? (a.getAttribute('href') || '') : '';
                            return {
                                province: tds[0].innerText.trim(),
                                city: tds[1].innerText.trim(),
                                xkz_num: tds[2].innerText.trim(),
                                company_name: tds[3].innerText.trim(),
                                industry: tds[4].innerText.trim(),
                                valid_period: tds[5].innerText.trim(),
                                publish_date: tds[6].innerText.trim(),
                                mgmt_type: tds[7].innerText.trim(),
                                detail_href: detailHref
                            };
                        }).filter(Boolean);
                    }""")

                    print(f"Page {current_p}: Found {len(items)} records.")

                    for idx, item in enumerate(items, start=1):
                        company = item['company_name']
                        xkz = item['xkz_num']
                        detail_href = item['detail_href']
                        detail_url = BASE_URL + detail_href if detail_href.startswith('/') else detail_href

                        clean_company = sanitize_filename(company)
                        clean_xkz = sanitize_filename(xkz)
                        pdf_filename = f"{clean_company}_{clean_xkz}_排污许可证副本.pdf"
                        save_path = os.path.join(OUTPUT_DIR, pdf_filename)

                        # Check if file already exists
                        if os.path.exists(save_path) and os.path.getsize(save_path) > 100:
                            print(f"  [{current_p}-{idx}] [Skipped] File exists: {pdf_filename}")
                            writer.writerow({
                                'page': current_p, 'index': idx,
                                'province': item['province'], 'city': item['city'],
                                'xkz_num': item['xkz_num'], 'company_name': item['company_name'],
                                'industry': item['industry'], 'valid_period': item['valid_period'],
                                'publish_date': item['publish_date'], 'mgmt_type': item['mgmt_type'],
                                'pdf_filename': pdf_filename, 'file_size': os.path.getsize(save_path),
                                'status': 'SUCCESS (EXISTS)', 'detail_url': detail_url, 'download_url': ''
                            })
                            csv_file.flush()
                            total_downloaded += 1
                            continue

                        # Open detail in new tab/page to isolate session
                        print(f"  [{current_p}-{idx}] Opening detail: {company} ({xkz})...")
                        detail_page = context.new_page()
                        pdf_download_url = None
                        status = 'FAILED'
                        file_size = 0

                        try:
                            detail_page.goto(detail_url, referer=LICENSE_URL, wait_until="networkidle", timeout=30000)
                            random_wait(1.5, 2.5)

                            # Locate PDF download link (fileType=fbfile or 排污许可证副本)
                            pdf_href = detail_page.evaluate("""() => {
                                const links = Array.from(document.querySelectorAll('a'));
                                const fbLink = links.find(a => (a.href && a.href.includes('fileType=fbfile')) || (a.innerText && a.innerText.includes('排污许可证副本')));
                                if (fbLink) return fbLink.getAttribute('href');
                                const anyDl = links.find(a => a.href && a.href.includes('downloadFile.action'));
                                return anyDl ? anyDl.getAttribute('href') : null;
                            }""")

                            if pdf_href:
                                pdf_download_url = BASE_URL + pdf_href if pdf_href.startswith('/') else pdf_href
                                # Download PDF using browser context API (inherits browser cookies, TLS, referer)
                                resp = page.request.get(pdf_download_url, headers={'Referer': detail_url})
                                if resp.status == 200:
                                    pdf_data = resp.body()
                                    if len(pdf_data) > 100:
                                        with open(save_path, 'wb') as f_pdf:
                                            f_pdf.write(pdf_data)
                                        file_size = len(pdf_data)
                                        status = 'SUCCESS'
                                        print(f"    -> [Downloaded] {pdf_filename} ({file_size} bytes)")
                                        total_downloaded += 1
                                    else:
                                        status = 'FAILED (EMPTY DATA)'
                                        print(f"    -> [Failed] Download returned empty data")
                                        total_failed += 1
                                else:
                                    status = f'FAILED (HTTP {resp.status})'
                                    print(f"    -> [Failed] Download HTTP {resp.status}")
                                    total_failed += 1
                            else:
                                status = 'FAILED (NO PDF LINK)'
                                print(f"    -> [Failed] No PDF link found on detail page")
                                total_failed += 1

                        except Exception as det_err:
                            print(f"    -> [Error] Detail page error: {det_err}")
                            status = f'FAILED ({det_err})'
                            total_failed += 1
                        finally:
                            detail_page.close()

                        # Write row to CSV manifest
                        writer.writerow({
                            'page': current_p, 'index': idx,
                            'province': item['province'], 'city': item['city'],
                            'xkz_num': item['xkz_num'], 'company_name': item['company_name'],
                            'industry': item['industry'], 'valid_period': item['valid_period'],
                            'publish_date': item['publish_date'], 'mgmt_type': item['mgmt_type'],
                            'pdf_filename': pdf_filename, 'file_size': file_size,
                            'status': status, 'detail_url': detail_url, 'download_url': pdf_download_url or ''
                        })
                        csv_file.flush()
                        random_wait(1, 2)

                    # Advance to next page if not reached max_pages
                    if current_p < self.max_pages:
                        current_p += 1
                        print(f"[Stealth] Navigating to page {current_p}...")
                        page.evaluate(f"() => {{ jumpPage2({current_p}); }}")
                        page.wait_for_load_state("networkidle")
                        random_wait(3, 5)
                    else:
                        break

            except Exception as main_err:
                print(f"[Stealth ERROR] Main automation error: {main_err}")

            finally:
                csv_file.close()
                browser.close()

            print("\n==================================================")
            print(f"Stealth Download Job Finished!")
            print(f"Total Downloaded/Existing: {total_downloaded}, Total Failed: {total_failed}")
            print(f"PDF Output Directory: {OUTPUT_DIR}")
            print(f"Manifest CSV File: {MANIFEST_CSV}")
            print("==================================================")

def main():
    parser = argparse.ArgumentParser(description="Stealth PDP Permit PDF Downloader")
    parser.add_argument("--start-page", type=int, default=1, help="Start page number")
    parser.add_argument("--max-pages", type=int, default=5, help="Max page number")
    parser.add_argument("--headful", action="store_true", help="Run browser in headful mode")
    args = parser.parse_args()

    downloader = StealthPermitDownloader(
        headless=not args.headful,
        start_page=args.start_page,
        max_pages=args.max_pages
    )
    downloader.run()

if __name__ == '__main__':
    main()
