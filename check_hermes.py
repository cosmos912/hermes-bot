import requests
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "あなたのURL"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8",
    "Referer": "https://www.hermes.com/jp/ja/"
}

def notify(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def check(url):
    session = requests.Session()
    res = session.get(url, headers=headers)

    print("status:", res.status_code)

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
