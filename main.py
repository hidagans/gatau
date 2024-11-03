import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def read_proxies_from_file(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies if proxy.strip()]

def run_playwright_with_proxy(proxy):
    user_agent = get_random_user_agent()
    logging.info(f'Starting worker with proxy: {proxy}')
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Non-headless mode
            context = browser.new_context(
                proxy={"server": proxy},
                user_agent=user_agent
            )
            page = context.new_page()

            # Mengunjungi website dengan referer
            referer_url = "https://yeari.tech"
            page.goto(referer_url)
            logging.info(f'Worker with proxy {proxy} visited the website.')

            time.sleep(random.uniform(2, 5))  # Random sleep to mimic human behavior

            # Mengunjungi direct link dengan referer
            direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
            page.goto(direct_link, referer=referer_url)  # Menambahkan referer
            logging.info(f'Worker with proxy {proxy} visited the direct link with referer.')

            time.sleep(random.uniform(2, 5))  # Random sleep to mimic human behavior

            browser.close()
        logging.info(f'Worker with proxy {proxy} has finished processing.')
    except Exception as e:
        logging.error(f'Worker with proxy {proxy} generated an exception: {e}')
        
def main(num_workers):
    proxies = read_proxies_from_file('proxy.txt')
    
    if proxies:
        logging.info(f'Starting {num_workers} workers.')
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(run_playwright_with_proxy, random.choice(proxies)): i for i in range(num_workers)}
            
            for future in futures:
                try:
                    future.result()  # Wait for task to finish
                except Exception as e:
                    logging.error(f'Worker generated an exception: {e}')
    else:
        logging.warning("No proxies found in proxy.txt")

if __name__ == "__main__":
    NUM_WORKERS = 5  # Number of workers to run
    main(NUM_WORKERS)
