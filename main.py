#!/usr/bin/env python
import argparse
from app.downloader import RobustPermitDownloader

def main():
    parser = argparse.ArgumentParser(description="PDP Permit Copy (排污许可证副本) Multi-Province Downloader")
    parser.add_argument("--province", "-p", type=str, default="吉林", help="Province name or code (e.g. 北京, 广东, 四川, 江苏, 吉林, 220000000000)")
    parser.add_argument("--start-page", "-s", type=int, default=1, help="Start page number (default: 1)")
    parser.add_argument("--max-pages", "-m", type=int, default=5, help="End page number (default: 5)")
    parser.add_argument("--proxy", type=str, default="", help="HTTP/HTTPS proxy URL (e.g. http://127.0.0.1:7897)")
    args = parser.parse_args()

    downloader = RobustPermitDownloader(
        province=args.province,
        proxy=args.proxy,
        start_page=args.start_page,
        max_pages=args.max_pages
    )
    downloader.run()

if __name__ == '__main__':
    main()
