#!/usr/bin/env python3
"""
Fetch AutoScout24 listing page with Selenium, parse with BeautifulSoup,
and print current HTML structure so the scraper can use the right selectors.
Run inside Docker: docker run --rm -v $(pwd):/app -w /app <image> python3 inspect_html.py
"""
import os
import re
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Install beautifulsoup4 first (pip install beautifulsoup4)")
    sys.exit(1)

# Optional: use Selenium to get JS-rendered HTML
USE_SELENIUM = os.environ.get("USE_SELENIUM", "1") == "1"
LISTING_URL = os.environ.get(
    "LISTING_URL",
    "https://www.autoscout24.com/lst?atype=C&cy=D&damage_list=0&desc=0&sort=age&page=1",
)


def get_html_with_selenium(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_bin = os.environ.get("CHROME_BIN")
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
    if chrome_bin:
        chrome_options.binary_location = chrome_bin
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(15)
    driver.get(url)
    import time
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html


def get_html_with_requests(url):
    import requests
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0"})
    r.raise_for_status()
    return r.text


def inspect_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    report = []

    # 1) Pagination
    report.append("=== PAGINATION ===")
    for sel in [
        "[class*='pagination']",
        "nav[aria-label*='agination']",
        "nav",
        "[role='navigation']",
    ]:
        els = soup.select(sel)
        if els:
            for el in els[:2]:
                buttons = el.find_all(["button", "a"])
                nums = []
                for b in buttons:
                    t = (b.get_text() or "").strip()
                    if t.isdigit():
                        nums.append(int(t))
                    if b.get("href") and "page=" in b.get("href", ""):
                        m = re.search(r"page=(\d+)", b.get("href", ""))
                        if m:
                            nums.append(int(m.group(1)))
                if nums:
                    report.append(f"  {sel}: found numbers {sorted(set(nums))[-5:]}")
    # Any element containing "page" and a number
    for tag in soup.find_all(class_=re.compile(r"page|pagination", re.I)):
        cls = tag.get("class", [])
        text = tag.get_text()
        if re.search(r"\d+", text):
            report.append(f"  class {cls}: text snippet: {text[:80]}")

    # 2) Offer count (header total)
    report.append("\n=== OFFER COUNT (header) ===")
    for sel in ["header h1", "h1", "[class*='ListHeader']", "[class*='header'] h1"]:
        els = soup.select(sel)
        for el in els[:3]:
            t = el.get_text()
            n = re.search(r"[\d,.\s]+", t)
            if n and re.search(r"\d", t):
                report.append(f"  {sel}: {t.strip()[:100]}")

    # 3) Main content and articles
    report.append("\n=== MAIN / ARTICLES ===")
    main = soup.find("main")
    if main:
        articles = main.find_all("article")
        report.append(f"  main found, articles inside: {len(articles)}")
        for i, art in enumerate(articles[:2]):
            a = art.find("a", href=re.compile(r"/offers/|/lst"))
            if a:
                report.append(f"  article[{i}] link: {a.get('href', '')[:80]}")
            # Classes on article
            report.append(f"  article[{i}] classes: {art.get('class', [])}")
    else:
        report.append("  no <main> found")
        articles = soup.find_all("article")
        report.append(f"  articles in body: {len(articles)}")
        for i, art in enumerate(articles[:2]):
            a = art.find("a", href=re.compile(r"autoscout24|/offers/"))
            if a:
                report.append(f"  article[{i}] link: {a.get('href', '')[:80]}")
            report.append(f"  article[{i}] classes: {art.get('class', [])}")

    # 4) Links that look like listing detail URLs
    report.append("\n=== LINKS (detail) ===")
    detail_links = soup.select('a[href*="/offers/"]')
    report.append(f"  a[href*='/offers/'] count: {len(detail_links)}")
    for a in detail_links[:3]:
        report.append(f"    {a.get('href', '')[:90]}")
        # Parent classes
        p = a.parent
        if p:
            report.append(f"      parent tag={p.name} class={p.get('class', [])}")

    # 5) All classes containing ListItem or Card (for article selector)
    report.append("\n=== CLASSES (ListItem/Card/Article) ===")
    seen = set()
    for tag in soup.find_all(class_=True):
        for c in tag.get("class", []):
            if any(x in c for x in ["ListItem", "Card", "Article", "listing", "item"]):
                if c not in seen:
                    seen.add(c)
                    report.append(f"  {c} (tag={tag.name})")

    return "\n".join(report)


def main():
    print("Fetching", LISTING_URL, "with", "Selenium" if USE_SELENIUM else "requests", "...")
    try:
        if USE_SELENIUM:
            html = get_html_with_selenium(LISTING_URL)
        else:
            html = get_html_with_requests(LISTING_URL)
    except Exception as e:
        print("Fetch failed:", e)
        sys.exit(1)

    print("\n" + inspect_listing(html))

    # Optionally save HTML for manual inspection
    out = os.environ.get("SAVE_HTML")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("\nSaved HTML to", out)


if __name__ == "__main__":
    main()
