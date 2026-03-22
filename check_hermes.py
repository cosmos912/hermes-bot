import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "https://www.hermes.com/jp/ja/product/%E3%83%90%E3%83%83%E3%82%B0-%E3%80%8A%E3%83%9C%E3%83%AA%E3%83%BC%E3%83%891923%E3%80%8B-%E3%83%9F%E3%83%8B-%E3%80%8A%E7%A9%BA%E6%83%B3%E3%81%AE%E9%9E%8D%E3%80%8B-H084257CKAB/"
]

def notify(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def check_stock(driver, url):
    driver.get(url)

    try:
        # ページ完全ロード待ち
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # さらに少し待つ（ここがミソ）
        time.sleep(3)

        # カートボタン検出
        driver.find_element(By.CSS_SELECTOR, "button[class*='add-to-cart']")

        print("在庫あり")
        return True

    except Exception as e:
        print("在庫なし or 未検出", e)
        return False

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    in_stock = []

    for url in URLS:
        result = check_stock(driver, url)
        print(url, result)

        if result:
            in_stock.append(url)

    driver.quit()

    if in_stock:
        notify("🔥在庫あり🔥\n" + "\n".join(in_stock))
    else:
        print("在庫なし")

if __name__ == "__main__":
    main()
