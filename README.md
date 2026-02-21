# AutoScout24 Data Collector

Backend service and CLI for collecting vehicle listing data from [AutoScout24](https://www.autoscout24.com) (listing URL → offers with title, model, vendor info, phone numbers).

## Setup

- **Python**: 3.10+
- **Chrome or Chromium** is required for scraping (the script uses Selenium). ChromeDriver is auto-downloaded when needed (via `webdriver-manager`).

```bash
pip install -r requirements.txt
```

### No Chrome or ChromeDriver?

If you see an error like *"Chrome or Chromium is required but not available"* or nothing happens:

1. **Use Docker (easiest)** – no Chrome needed on your machine:
   ```bash
   docker build -t autoscout24 .
   docker run -p 3000:3000 autoscout24
   ```
   Then call `POST http://localhost:3000/scrape` or run the collector inside the container.

2. **Install Chrome** – [Google Chrome](https://www.google.com/chrome/) or Chromium. On Linux (Debian/Ubuntu): `sudo apt install chromium chromium-driver`. Then run `pip install -r requirements.txt` again; the driver is auto-fetched if needed.

## Run as API (Flask)

```bash
python app.py
# Server: http://0.0.0.0:3000
```

- **GET /** – service info and docs  
- **GET /health** – health check  
- **POST /scrape** – collect offers (JSON body below)

### POST /scrape

| Field          | Required | Description |
|----------------|----------|-------------|
| `url`          | yes      | AutoScout24 listing URL (e.g. `https://www.autoscout24.com/lst?atype=C&cy=D&...`) |
| `number`       | yes      | Number of offers to collect (1–500) |
| `startPage`    | no       | Start from this page (default: 1) |
| `waitingTime`  | no       | Selenium wait in seconds (default: 30) |
| `businessType` | no       | `b2b` or `b2c` (filter by phone prefix, default: b2b) |

Example:

```bash
curl -X POST http://localhost:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.autoscout24.com/lst?atype=C&cy=D&page=1", "number": 10}'
```

## Run as CLI (data collector)

Collect offers and write to a JSON file or stdout:

```bash
python collect.py "https://www.autoscout24.com/lst?atype=C&cy=D&page=1" --number 20 --out offers.json
python collect.py "https://www.autoscout24.com/lst?..." -n 50 --start-page 2 --business-type b2c
```

Options: `--number` / `-n`, `--start-page`, `--waiting-time`, `--business-type`, `--out` / `-o`, `--no-pretty`.

## Docker

Build and run:

```bash
docker build -t autoscout24-collector .
docker run -p 3000:3000 autoscout24-collector
```

Override port: `-e PORT=8080`. Optional debug log: `-e AUTOSCOUT24_DEBUG_LOG=/tmp/debug.log`.

## Inspect HTML (debugging selectors)

When the site layout changes, use the inspector to see current structure:

```bash
# Uses Selenium by default
USE_SELENIUM=1 LISTING_URL="https://www.autoscout24.com/lst?..." python inspect_html.py
# Save HTML to file
SAVE_HTML=listing.html USE_SELENIUM=1 python inspect_html.py
```

## Environment

| Variable               | Description |
|------------------------|-------------|
| `PORT`                 | Flask port (default: 3000) |
| `AUTOSCOUT24_DEBUG_LOG`| If set, append debug logs to this file |
| `CHROME_BIN`           | (Docker) Path to Chromium binary |
| `CHROMEDRIVER_PATH`    | (Docker) Path to ChromeDriver |

## Response shape

- **success**: boolean  
- **count**: number of offers collected  
- **data**: list of `{ "url": "<offer URL>", "data": { "title", "model", "vendor_info": { "name", "address", "company", "numbers", ... } } }`  
- **meta**: `offers_requested`, `offers_collected`, `num_of_pages`, `errors`, etc.
