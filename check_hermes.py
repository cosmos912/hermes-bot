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

    matches = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        re.DOTALL
    )

    if not matches:
        print("JSON見つからない")
        return None

    for m in matches:
        try:
            data = json.loads(m)

            # パターン①
            if isinstance(data, dict):
                offers = data.get("offers")
                if offers:
                    availability = offers.get("availability", "")
                    if "InStock" in availability:
                        return True
                    elif "OutOfStock" in availability:
                        return False

            # パターン②（配列で来る場合）
            if isinstance(data, list):
                for item in data:
                    offers = item.get("offers")
                    if offers:
                        availability = offers.get("availability", "")
                        if "InStock" in availability:
                            return True
                        elif "OutOfStock" in availability:
                            return False

        except Exception as e:
            continue

    return None

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
