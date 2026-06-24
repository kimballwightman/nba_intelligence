"""
Scrapes salary/cap data from SalarySwish.
Outputs CSVs to data/scrapers/output/.

Usage:
    python salaryswish.py

TODO: inspect the specific pages on salaryswish.com to identify
the right selectors and which pages to target (cap space, apron, etc).
"""

import csv
import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def scrape_page(url: str, output_filename: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # TODO: replace with the actual selector after inspecting the page
        # page.wait_for_selector("YOUR_SELECTOR_HERE")

        browser.close()

    print(f"TODO: implement selector logic for {url}")


if __name__ == "__main__":
    # TODO: add the specific SalarySwish page URLs once inspected
    scrape_page("https://www.salaryswish.com/", "salaryswish.csv")
