import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URLS = [
    "https://www.hermes.com/jp/ja/product/バッグ-《ボリード1923》-ミニ-H084257CKAB/"
]

def notify(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def check_stock(driver, url):
    driver.get(url)

    try:
        # カートボタン探す
        driver.find_element(By.CSS_SELECTOR, "button[class*='add-to-cart']")
        return True
    except:
        return False

def main():
    options = Options()
    options.add_argument("--headless")
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
