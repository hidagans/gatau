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

def get_random_referer():
    referers = [
        "https://www.pinterest.com",
        "https://web.telegram.org",
        "https://www.instagram.com",
        "https://www.facebook.com",
        "https://www.twitter.com",
        "https://www.linkedin.com",
        "https://www.reddit.com",
        "https://www.tiktok.com",
        "https://www.quora.com",
        "https://www.youtube.com",
        "https://www.whatsapp.com",
        "https://www.snapchat.com",
        "https://www.flickr.com",
        "https://www.tumblr.com",
        "https://www.medium.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.paypal.com",
        "https://www.booking.com",
        # Tambahkan lebih banyak referer sesuai kebutuhan
    ]
    return random.choice(referers)

def read_proxies_from_file(filename):
    try:
        with open(filename, 'r') as file:
            proxies = file.readlines()
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except FileNotFoundError:
        logging.error("File proxy.txt tidak ditemukan!")
        return []

def simulate_user_behavior(page):
    for _ in range(3):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.1, 0.5))
    
    if random.random() < 0.5:
        page.mouse.click(random.randint(0, 1280), random.randint(0, 720))

    page.mouse.wheel(0, random.randint(100, 500))
    time.sleep(random.uniform(1, 3))

def run_playwright_with_proxy(proxy_url):
    parsed_proxy = urlparse(proxy_url)
    user_agent = get_random_user_agent()
    referer_url = get_random_referer()
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

            direct_link = "https://yeari.tech"
            logging.info(f'Navigating to {referer_url} using proxy {proxy_url}')
            page.goto(referer_url, timeout=30000)
            logging.info(f'Visited referer page.')

            time.sleep(random.uniform(15, 30))

            logging.info(f'Navigating to {direct_link} using referer {referer_url}')
            page.goto(direct_link, referer=referer_url, timeout=30000)
            logging.info(f'Visited direct link with referer.')

            simulate_user_behavior(page)

            time.sleep(random.uniform(30, 60))

            context.close()
            browser.close()
        logging.info(f'Worker with proxy {proxy_url} has finished processing.')
    except Exception as e:
        logging.error(f'Worker with proxy {proxy_url} generated an exception: {e}')

def main():
    proxies = read_proxies_from_file('proxy.txt')

    if not proxies:
        logging.warning("No proxies found in proxy.txt")
        return

    num_workers = len(proxies)  # Set jumlah worker sesuai jumlah proxy

    while True:
        logging.info(f'Starting {num_workers} workers based on available proxies.')
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(run_playwright_with_proxy, proxy): proxy for proxy in proxies}
            
            for future in futures:
                try:
                    future.result()  # Wait for task to finish
                except Exception as e:
                    logging.error(f'Worker generated an exception: {e}')
        
        delay = random.randint(5 * 60, 30 * 60)
        logging.info(f'All workers completed. Waiting for {delay / 60} minutes before starting new batch.')
        time.sleep(delay)

if __name__ == "__main__":
    main()
