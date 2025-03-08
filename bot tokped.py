from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

# Path ke ChromeDriver
CHROMEDRIVER_PATH = r"C:\Chromedriver\chromedriver.exe"  # Sesuaikan path dengan sistem Anda

# Inisialisasi Chrome Options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("--no-sandbox")  
# options.add_argument("--headless")  # Hapus tanda "#" jika ingin menjalankan tanpa tampilan browser

# Inisialisasi WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Buka Tokopedia
driver.get("https://www.tokopedia.com/")
time.sleep(3)  # Tunggu sebentar agar halaman terbuka dengan sempurna

# Path ke file cookies
COOKIES_PATH = r"C:\Chromedriver\www.tokopedia.com.cookies.json"  # Sesuaikan path

def load_cookies():
    """Memuat cookies dari file JSON dan menerapkannya ke browser."""
    try:
        with open(COOKIES_PATH, "r") as file:
            cookies = json.load(file)

        valid_cookies = [cookie for cookie in cookies if "domain" in cookie and "tokopedia.com" in cookie["domain"]]

        for cookie in valid_cookies:
            driver.add_cookie(cookie)  # Menambahkan hanya cookies yang sesuai

        # Refresh agar cookies diterapkan
        driver.refresh()
        time.sleep(3)
        print("✅ Login berhasil dengan cookies!")

    except FileNotFoundError:
        print("❌ File cookies tidak ditemukan! Silakan login secara manual dan simpan cookies.")

# URL Produk Flash Sale
PRODUCT_URL = "https://www.tokopedia.com/unilever/rinso-matic-deterjen-cair-mesin-bukaan-depan-1-45l-twin-pack?extParam=src%3Dmultiloc%26whid%3D5490&aff_unique_id=&channel=others&chain_key="

def flash_sale():
    """Menjalankan pembelian produk Flash Sale secara otomatis."""
    max_attempts = 5  # Jumlah maksimum percobaan reload
    attempt = 0

    while attempt < max_attempts:
        try:
            # Buka halaman produk flash sale
            driver.get(PRODUCT_URL)

            # Tunggu sampai tombol "Beli Sekarang" muncul
            buy_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[4]/div[1]/button[2]/span"))
            )
            buy_button.click()

            # Tunggu sampai halaman checkout muncul
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/section[2]/div[2]/button/span"))
            )
            print("✅ Berhasil menambahkan produk ke keranjang!")
            break  # Keluar dari loop jika berhasil

        except TimeoutException:
            print(f"❌ Flash sale sudah habis atau produk tidak ditemukan. Mencoba lagi... ({attempt + 1}/{max_attempts})")
            attempt += 1
            time.sleep(2)  # Tunggu 2 detik sebelum reload
            continue  # Lanjut ke iterasi berikutnya

        except NoSuchElementException:
            print(f"❌ Tombol 'Beli Sekarang' tidak ditemukan. Mencoba lagi... ({attempt + 1}/{max_attempts})")
            attempt += 1
            time.sleep(2)  # Tunggu 2 detik sebelum reload
            continue  # Lanjut ke iterasi berikutnya

    if attempt == max_attempts:
        print("❌ Gagal setelah mencoba beberapa kali. Flash sale mungkin sudah habis.")

if __name__ == "__main__":
    try:
        load_cookies()  # Memuat cookies sebelum membeli
        flash_sale()  # Eksekusi pembelian flash sale
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
    finally:
        # Tetap biarkan browser terbuka setelah selesai
        print("✅ Proses selesai. Browser tetap terbuka.")
        input("Tekan Enter untuk menutup browser...")  # Tunggu input pengguna sebelum menutup
        driver.quit()  # Tutup browser setelah pengguna menekan Enter