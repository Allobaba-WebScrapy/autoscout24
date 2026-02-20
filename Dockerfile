# Single container: Python + Chromium + ChromeDriver (no Chrome needed on host)
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install Chromium and ChromeDriver from Debian + runtime deps Chrome needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    # Chrome/Chromium runtime dependencies
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py AutoScout24.py collect.py fallback_data.py .

EXPOSE 3000

CMD ["python3", "app.py"]
