import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def read_proxies_from_file(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies if proxy.strip()]

def run_playwright_with_proxy(proxy_url):
    parsed_proxy = urlparse(proxy_url)
    user_agent = get_random_user_agent()
    logging.info(f'Starting worker with proxy: {proxy_url}')
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                proxy={
                    "server": f"{parsed_proxy.scheme}://{parsed_proxy.hostname}:{parsed_proxy.port}",
                    "username": parsed_proxy.username,
                    "password": parsed_proxy.password
                },
                user_agent=user_agent
            )
            page = context.new_page()

            referer_url = "https://yeari.tech"
            logging.info(f'Navigating to {referer_url} using proxy {proxy_url}')
            page.goto(referer_url)
            logging.info(f'Worker with proxy {proxy_url} visited the website.')

            time.sleep(random.uniform(2, 5))

            direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
            logging.info(f'Navigating to {direct_link} using referer {referer_url}')
            page.goto(direct_link, referer=referer_url)
            logging.info(f'Worker with proxy {proxy_url} visited the direct link with referer.')

            time.sleep(random.uniform(2, 5))

            browser.close()
        logging.info(f'Worker with proxy {proxy_url} has finished processing.')
    except Exception as e:
        logging.error(f'Worker with proxy {proxy_url} generated an exception: {e}')
        
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
    NUM_WORKERS = 1  # Number of workers to run
    main(NUM_WORKERS)
