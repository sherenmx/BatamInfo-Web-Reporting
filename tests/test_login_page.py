from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


class TestLoginPage:
    def setup_method(self, method):
        """Inisialisasi WebDriver dan buka halaman Login sebelum setiap test."""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:5000/login"
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(5)

    def teardown_method(self, method):
        """Tutup browser setelah setiap test."""
        self.driver.quit()

    def checkElement(self, locator_type, locator_value):
        """Memeriksa keberadaan elemen di halaman login."""
        try:
            if locator_type.lower() == 'name':
                self.driver.find_element(By.NAME, locator_value)
            elif locator_type.lower() == 'id':
                self.driver.find_element(By.ID, locator_value)
            print(f"[PASS] Elemen '{locator_value}' ditemukan.")
            return True
        except:
            print(f"[FAIL] Elemen '{locator_value}' TIDAK ditemukan.")
            return False

    def solve_captcha(self):
        """
        Membaca teks di layar untuk menemukan soal matematika (misal: "5 + 7"),
        menghitungnya, dan mengembalikan hasil penjumlahannya.
        """
        try:
            # Ambil seluruh teks yang ada di body halaman
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Cari pola angka + angka menggunakan Regex
            match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
            if match:
                angka1 = int(match.group(1))
                angka2 = int(match.group(2))
                hasil = angka1 + angka2
                print(f"[INFO] Bot membaca CAPTCHA: {angka1} + {angka2} = {hasil}")
                return str(hasil)
            else:
                print("[WARNING] Pola CAPTCHA tidak ditemukan di layar.")
                return "0"
        except Exception as e:
            print(f"[ERROR] Gagal membaca CAPTCHA: {e}")
            return "0"

    def attempt_login(self, username, password, captcha_answer):
        """Fungsi pembantu untuk mengisi form dan menekan tombol login."""
        time.sleep(1)  # Jeda visual
        # Biarkan exception mengemuka agar pytest bisa menangkap kegagalan.
        user_field = self.driver.find_element(By.NAME, "username")
        user_field.clear()
        user_field.send_keys(username)

        pass_field = self.driver.find_element(By.NAME, "password")
        pass_field.clear()
        pass_field.send_keys(password)

        captcha_field = self.driver.find_element(By.NAME, "captcha")
        captcha_field.clear()
        captcha_field.send_keys(captcha_answer)

        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()
        time.sleep(2)  # Tunggu respons dari server

    # --- VARIASI TEST CASE ---
    def test_wrong_captcha(self):
        """Test Case 1: Username & Password BENAR, tapi CAPTCHA SALAH"""
        # Masukkan kredensial yang valid, tapi captcha disengaja salah ("999")
        self.attempt_login("admin", "AdminUVERS2026!", "999")
        assert "login" in self.driver.current_url, "Sistem seharusnya menolak login karena CAPTCHA salah"

    def test_wrong_credentials(self):
        """Test Case 2: Username/Password SALAH, tapi CAPTCHA BENAR"""
        jawaban_benar = self.solve_captcha()
        self.attempt_login("hacker", "password123", jawaban_benar)
        assert "login" in self.driver.current_url, "Sistem seharusnya menolak kredensial yang salah"

    def test_success_login(self):
        """Test Case 3: Username, Password, dan CAPTCHA BENAR (Happy Path)"""
        # Muat ulang halaman untuk mendapatkan soal CAPTCHA baru
        self.driver.get(self.base_url)
        jawaban_benar = self.solve_captcha()

        # Sesuaikan username/password sesuai data di aplikasi Anda
        self.attempt_login("mhs1", "123", jawaban_benar)

        assert ("dashboard" in self.driver.current_url.lower()) or (self.driver.current_url != self.base_url), "Seharusnya dialihkan ke dashboard setelah login berhasil"

    # tidak perlu closeBrowser karena pytest akan memanggil teardown_method
