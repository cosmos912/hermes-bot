print("★★★このコード動いてる★★★")

import requests
import re
import json
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%AA%E3%83%BC%E3%83%891923-%E3%83%9F%E3%83%8B-H084257CKAB/"
]

def notify(message):
    webhook_url = os.environ.get("SLACK_WEBHOOK")

    print("送信するよ")

    res = requests.post(
        webhook_url,
        json={"text": message}
    )

    print("Status:", res.status_code)
    print("Response:", res.text)

def check_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    html = res.text

    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)

    if not match:
        return None

    data = json.loads(match.group(1))
    offers = data.get("offers", {})
    availability = offers.get("availability", "")

    return "InStock" in availability

def main():
    in_stock_urls = []

    for url in URLS:
        result = check_stock(url)
        print(url, "→", result)  # デバッグ用

        if result:
            in_stock_urls.append(url)

    if in_stock_urls:
        message = "🔥在庫あり🔥\n" + "\n".join(in_stock_urls)
        notify(message)
    else:
        print("在庫なし")
        
if __name__ == "__main__":
    main()
