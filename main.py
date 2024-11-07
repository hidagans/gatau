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
    # Simulasi gerakan kursor acak
    for _ in range(5):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.2, 0.8))

    # Simulasi hover di area iklan tanpa klik langsung
    hover_x, hover_y = random.randint(200, 600), random.randint(100, 400)
    page.mouse.move(hover_x, hover_y)
    logging.info(f"Hovering near ad area at {hover_x}, {hover_y}")
    time.sleep(random.uniform(2, 5))  # Stay near ad for a few seconds

    # Gulir ke bawah secara bertahap
    for _ in range(3):
        page.mouse.wheel(0, random.randint(200, 500))
        time.sleep(random.uniform(1, 2))  # Tunda sedikit antara scroll

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

            # Arahkan ke halaman Anda
            page.goto("https://yeari.tech")
            page.wait_for_selector("body", timeout=60000)  # Menunggu 60 detik untuk body dimuat
            # Tunggu hingga elemen pop-up muncul
            page.wait_for_selector('div[data-element="overlay"]')  # Tunggu overlay muncul
            
            # Klik tombol "OK" atau "CANCEL"
            try:
                # Cek apakah tombol OK muncul dan klik
                page.click('div[data-element="primary-button"]')  # Tombol OK
            except:
                # Jika tombol OK tidak ada, coba tombol CANCEL
                page.click('span[data-element="close-button"]')  # Tombol CANCEL

            # Simulasi perilaku menavigasi situs
            time.sleep(random.uniform(15, 30))
            # Simulasikan perilaku pengguna (scroll dan hover di area tertentu)
            simulate_user_behavior(page)

            # Tunda sebelum keluar agar kunjungan terlihat lebih lama
            time.sleep(random.uniform(30, 60))

            context.close()
            browser.close()
        logging.info(f'Worker with proxy {proxy_url} has finished processing.')
    except Exception as e:
        logging.error(f'Worker with proxy {proxy_url} generated an exception: {e}')

def main(num_workers):
    proxies = read_proxies_from_file('proxy.txt')

    if not proxies:
        logging.warning("No proxies found in proxy.txt")
        return

    while True:
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
