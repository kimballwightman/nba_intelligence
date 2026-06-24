"""
Scrapes player and team salary tables from HoopsHype.
Outputs CSVs to data/scrapers/output/.

Usage:
    python hoopshype_salaries.py
"""

import csv
import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def scrape_player_salaries():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.hoopshype.com/salaries/players/")
        page.wait_for_selector("table.hh-salaries-ranking-table")

        rows = page.query_selector_all("table.hh-salaries-ranking-table tr")
        headers = [th.inner_text().strip() for th in rows[0].query_selector_all("th,td")]

        data = []
        for row in rows[1:]:
            cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if cells:
                data.append(cells)

        browser.close()

    out_path = os.path.join(OUTPUT_DIR, "hoopshype_player_salaries.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Wrote {len(data)} rows to {out_path}")


def scrape_team_salaries():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.hoopshype.com/salaries/teams/")
        page.wait_for_selector("table.hh-salaries-ranking-table")

        rows = page.query_selector_all("table.hh-salaries-ranking-table tr")
        headers = [th.inner_text().strip() for th in rows[0].query_selector_all("th,td")]

        data = []
        for row in rows[1:]:
            cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if cells:
                data.append(cells)

        browser.close()

    out_path = os.path.join(OUTPUT_DIR, "hoopshype_team_salaries.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Wrote {len(data)} rows to {out_path}")


if __name__ == "__main__":
    scrape_player_salaries()
    scrape_team_salaries()
