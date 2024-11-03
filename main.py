import random
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

# Fungsi untuk memilih user agent secara acak
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Fungsi untuk menjalankan Playwright
def run_playwright():
    user_agent = get_random_user_agent()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Anda juga bisa menggunakan p.firefox()
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Mengunjungi website
        page.goto("https://yeari.tech")
        print("Website visited")

        # Klik direct link Adsterra
        direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
        page.goto(direct_link)
        print("Direct link visited")

        # Tunggu beberapa detik untuk melihat hasil (jika diperlukan)
        page.wait_for_timeout(5000)

        # Menutup browser
        browser.close()

if __name__ == "__main__":
    run_playwright()
