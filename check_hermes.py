import requests
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%9C%E3%83%AA%E3%83%BC%E3%83%891923%E3%80%8B-%E3%83%9F%E3%83%8B-%E3%80%8A%E7%A9%BA%E6%83%B3%E3%81%AE%E9%9E%8D%E3%80%8B-H084257CKAB/"
]

def notify(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def check(url):
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return res.status_code == 200

def main():
    alive = []

    for url in URLS:
        ok = check(url)
        print(url, ok)

        if ok:
            alive.append(url)

    if alive:
        notify("🟢ページ復活\n" + "\n".join(alive))
    else:
        print("全部404")

if __name__ == "__main__":
    main()
