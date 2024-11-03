import random
import logging
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fungsi untuk memilih user agent secara acak
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Fungsi untuk membaca proxy dari file
def read_proxies_from_file(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies if proxy.strip()]

# Fungsi untuk menjalankan Playwright dengan proxy
def run_playwright_with_proxy(proxy):
    user_agent = get_random_user_agent()
    
    logging.info(f'Starting worker with proxy: {proxy}')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            proxy={"server": proxy},
            user_agent=user_agent
        )
        page = context.new_page()

        # Mengunjungi website
        page.goto("https://yeari.tech")
        logging.info(f'Worker with proxy {proxy} visited the website.')

        # Klik direct link Adsterra
        direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
        page.goto(direct_link)
        logging.info(f'Worker with proxy {proxy} visited the direct link.')

        # Tunggu beberapa detik untuk melihat hasil (jika diperlukan)
        page.wait_for_timeout(5000)

        # Menutup browser
        browser.close()
    
    logging.info(f'Worker with proxy {proxy} has finished processing.')

def main(num_workers):
    proxies = read_proxies_from_file('proxy.txt')
    
    if proxies:
        logging.info(f'Starting {num_workers} workers.')
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Pilih proxy secara acak untuk setiap worker
            futures = {executor.submit(run_playwright_with_proxy, random.choice(proxies)): i for i in range(num_workers)}
            
            for future in futures:
                try:
                    future.result()  # Tunggu hingga task selesai
                except Exception as e:
                    logging.error(f'Worker generated an exception: {e}')
    else:
        logging.warning("No proxies found in proxy.txt")

if __name__ == "__main__":
    NUM_WORKERS = 5  # Jumlah worker yang ingin Anda jalankan
    main(NUM_WORKERS)
