import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright, TimeoutError
from fake_useragent import UserAgent
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def read_proxies_from_file(filename):
    try:
        with open(filename, 'r') as file:
            proxies = file.readlines()
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except FileNotFoundError:
        logging.error("File proxy.txt tidak ditemukan!")
        return []

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
            direct_link = "https://www.profitablecpmrate.com/t3zqjex2ce?key=542325135c7996733951da8e62b9d900"

            logging.info(f'Navigating to {referer_url} using proxy {proxy_url}')
            page.goto(referer_url, timeout=30000)  # Timeout setelah 30 detik
            logging.info(f'Worker with proxy {proxy_url} visited the website.')

            time.sleep(random.uniform(15, 30))

            logging.info(f'Navigating to {direct_link} using referer {referer_url}')
            page.goto(direct_link, referer=referer_url, timeout=30000)

            # Menunggu pengalihan sampai mencapai URL akhir
            last_url = page.url
            for _ in range(10):  # Maksimal 10 kali pengecekan pengalihan
                time.sleep(3)  # Beri waktu jeda agar pengalihan terjadi
                if page.url != last_url:
                    logging.info(f'Redirected to: {page.url}')
                    last_url = page.url  # Update URL yang saat ini diakses
                else:
                    break  # Keluar jika URL tidak berubah, artinya pengalihan selesai

            logging.info(f'Final URL after possible redirects: {page.url}')

            time.sleep(random.uniform(30, 60))
            context.close()
            browser.close()
        logging.info(f'Worker with proxy {proxy_url} has finished processing.')
    except TimeoutError:
        logging.error(f'Worker with proxy {proxy_url} encountered a timeout error.')
    except Exception as e:
        logging.error(f'Worker with proxy {proxy_url} generated an exception: {e}')

def main(num_workers):
    proxies = read_proxies_from_file('proxy.txt')
    
    if not proxies:
        logging.warning("No proxies found in proxy.txt")
        return

    while True:  # Loop untuk memastikan program berjalan terus menerus
        logging.info(f'Starting {num_workers} workers.')
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(run_playwright_with_proxy, random.choice(proxies)): i for i in range(num_workers)}
            
            for future in futures:
                try:
                    future.result()  # Wait for task to finish
                except Exception as e:
                    logging.error(f'Worker generated an exception: {e}')
        
        # Delay acak antara 5 hingga 30 menit setelah semua worker selesai
        delay = random.randint(5 * 60, 30 * 60)
        logging.info(f'All workers completed. Waiting for {delay / 60} minutes before starting new batch.')
        time.sleep(delay)

if __name__ == "__main__":
    NUM_WORKERS = 10  # Jumlah worker yang akan dijalankan
    main(NUM_WORKERS)
