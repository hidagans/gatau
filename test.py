from playwright.sync_api import sync_playwright
import logging
import random
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_user_agent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

def run_playwright():
    user_agent = get_random_user_agent()
    logging.info('Starting worker without proxy')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Atur headless=True untuk mode tanpa tampilan
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        referer_url = "https://yeari.tech"  # URL referer yang diinginkan
        page.goto(referer_url)
        logging.info('Visited the website without proxy.')

        time.sleep(random.uniform(2, 5))  # Random sleep to mimic human behavior

        direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
        page.goto(direct_link, referer=referer_url)  # Menambahkan referer
        logging.info('Visited the direct link with referer.')

        time.sleep(random.uniform(2, 5))  # Random sleep to mimic human behavior

        browser.close()
    logging.info('Finished processing without proxy.')

if __name__ == "__main__":
    run_playwright()
