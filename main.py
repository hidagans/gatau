import random
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

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
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            proxy={"server": proxy},
            user_agent=user_agent
        )
        page = context.new_page()

        # Mengunjungi website
        page.goto("https://yeari.tech")
        print("Website visited with proxy:", proxy)

        # Klik direct link Adsterra
        direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
        page.goto(direct_link)
        print("Direct link visited with proxy:", proxy)

        # Tunggu beberapa detik untuk melihat hasil (jika diperlukan)
        page.wait_for_timeout(5000)

        # Menutup browser
        browser.close()

if __name__ == "__main__":
    proxies = read_proxies_from_file('proxy.txt')
    if proxies:
        # Pilih proxy secara acak
        selected_proxy = random.choice(proxies)
        run_playwright_with_proxy(selected_proxy)
    else:
        print("No proxies found in proxy.txt")
