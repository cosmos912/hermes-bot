import requests
import re
import json
import os

# Slack Webhook（GitHub Secretsから取得）
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

# 監視URL
URLS = [
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%B3%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CC10/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%B3%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CCI2/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%B3%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CC18/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%B3%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CC3Y/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CC37/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CC89/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%94%E3%82%BF%E3%83%B3%E3%83%BB%E3%83%AD%E3%83%83%E3%82%AF%E3%80%8B-18-H056289CCM4/",
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%9C%E3%83%AA%E3%83%BC%E3%83%891923%E3%80%8B-%E3%83%9F%E3%83%8B-%E3%80%8A%E7%A9%BA%E6%83%B3%E3%81%AE%E9%9E%8D%E3%80%8B-H084257CKAB/"
]

def notify(message):
    requests.post(
        SLACK_WEBHOOK,
        json={"text": message}
    )

def check_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    html = res.text

    # ld+json抽出
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)

    if not match:
        return None

    data = json.loads(match.group(1))
    offers = data.get("offers", {})
    availability = offers.get("availability", "")

    if "InStock" in availability:
        return True
    else:
        return False

def main():
    in_stock_urls = []

    for url in URLS:
        result = check_stock(url)
        if result:
            in_stock_urls.append(url)

    if in_stock_urls:
        message = "🔥在庫あり🔥\n" + "\n".join(in_stock_urls)
        notify(message)
    else:
        print("在庫なし")

if __name__ == "__main__":
    main()
