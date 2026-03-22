import requests
import re
import json
import os

print("★★★このコード動いてる★★★")

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%AA%E3%83%BC%E3%83%891923-%E3%83%9F%E3%83%8B-H084257CKAB/"
]

def notify(message):
    print("送信するよ")

    res = requests.post(
        SLACK_WEBHOOK,
        json={"text": message}
    )

    print("Status:", res.status_code)
    print("Response:", res.text)


def check_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    html = res.text

    # =========================
    # ① JSONチェック
    # =========================
    matches = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        re.DOTALL
    )

    print("JSON数:", len(matches))

    for m in matches:
        try:
            data = json.loads(m)

            # dictパターン
            if isinstance(data, dict):
                offers = data.get("offers")
                if offers:
                    availability = offers.get("availability", "")
                    if "InStock" in availability:
                        print("JSONで在庫あり検知")
                        return True
                    elif "OutOfStock" in availability:
                        return False

            # listパターン
            if isinstance(data, list):
                for item in data:
                    offers = item.get("offers")
                    if offers:
                        availability = offers.get("availability", "")
                        if "InStock" in availability:
                            print("JSONで在庫あり検知")
                            return True
                        elif "OutOfStock" in availability:
                            return False

        except:
            continue

    # =========================
    # ② HTMLチェック（強い）
    # =========================
    if "カートに追加" in html or "Add to cart" in html:
        print("HTMLで在庫あり検知")
        return True

    if "在庫なし" in html or "Out of stock" in html:
        return False

    # =========================
    # ③ 不明
    # =========================
    print("判定できず")
    return None


def main():
    print("★★★main入った★★★")

    in_stock_urls = []

    for url in URLS:
        result = check_stock(url)
        print(url, "→", result)

        if result:
            in_stock_urls.append(url)

    if in_stock_urls:
        message = "🔥在庫あり🔥\n" + "\n".join(in_stock_urls)
        notify(message)
    else:
        print("在庫なし")


if __name__ == "__main__":
    main()
