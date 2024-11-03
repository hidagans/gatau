import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time

# Fungsi untuk membaca proxy dari file
def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

# Fungsi untuk memilih user agent secara acak
def get_random_user_agent():
    ua = UserAgent()
    user_agents = [
        ua.random,  # User agent acak
        ua.android,  # User agent untuk Android
        ua.iphone,    # User agent untuk iPhone
        ua.chrome,    # User agent untuk Chrome desktop
        ua.firefox,   # User agent untuk Firefox desktop
    ]
    return random.choice(user_agents)

# Load proxy dari file
proxies = load_proxies('proxy.txt')

# Mengatur opsi untuk Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan di background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Pilih proxy secara acak
proxy = random.choice(proxies)
chrome_options.add_argument(f'--proxy-server={proxy}')

# Set user agent acak
user_agent = get_random_user_agent()
chrome_options.add_argument(f'user-agent={user_agent}')

# Ganti path ke chromedriver Anda
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Mengunjungi website
    driver.get("https://yeari.tech")
    time.sleep(3)  # Tunggu beberapa detik untuk memuat halaman

    # Mengklik direct link Adsterra
    direct_link = "https://www.profitablecpmrate.com/b1ybe1zgqj?key=638cfc32d59378f6618857b1192b5652"
    driver.get(direct_link)
    time.sleep(5)  # Tunggu beberapa detik untuk memuat halaman iklan

finally:
    driver.quit()  # Menutup browser
