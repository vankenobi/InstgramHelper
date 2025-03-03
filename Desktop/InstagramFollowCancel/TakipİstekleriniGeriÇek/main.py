from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import json

def login_instagram(driver, username, password):
    # Instagram giriş sayfasına git
    driver.get("https://www.instagram.com/accounts/login/")

    # Giriş sayfası yüklendikten sonra bekleyelim
    time.sleep(2)

    # Kullanıcı adı ve şifre alanlarını bul ve XPath'e göre etkileşimde bulun
    username_field = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
    password_field = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')

    # Kullanıcı adı ve şifreyi gir
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Giriş yap butonunu bul ve tıkla
    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]')
    login_button.click()

    # Giriş işlemi tamamlanana kadar bekleyelim
    time.sleep(5)

    # Eğer giriş başarılıysa, ana sayfa açılacaktır
    if "Instagram" in driver.title:
        print("Başarıyla giriş yapıldı!")
    else:
        print("Giriş yapılamadı, bilgilerinizi kontrol edin.")

# JSON verisinden kullanıcı adlarını al
with open('pending_follow_requests.json') as file:
    data = json.load(file)

usernames = []
for item in data["relationships_follow_requests_sent"]:
    if "string_list_data" in item and item["string_list_data"]:
        usernames.append(item["string_list_data"][0]["value"])  # Kullanıcı adını al

# Selenium ile işlemler
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/musakucuk/Library/Application Support/Google/Chrome/CustomProfile")
options.add_argument("--profile-directory=Default")  # Varsayılan Chrome profili
options.add_argument("--start-maximized")  # Tarayıcı tam ekran başlatılır

# WebDriver'ı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # Instagram giriş bilgilerinizi buraya girin
# username = "usernamegir"
# password = "passwordgir"

# # Giriş yap
# login_instagram(driver, username, password)

# Takip isteklerini geri çekme işlemi
for username in usernames:
    try:
        # Kullanıcı sayfasını aç
        driver.get(f'https://www.instagram.com/{username}/')

        time.sleep(0.8)
        text = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[2]/div/div/button/div/div').text
        if(text == "Requested"):

            # "İstek Gönderildi" butonuna tıkla
            time.sleep(0.8)
            follow_request_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[2]/div/div/button')
            follow_request_button.click()

            # "Takibi Bırak" butonuna tıkla
            time.sleep(1)
            unfollow_button = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/button[1]')
            unfollow_button.click()

            print(f"{username} adlı kullanıcıdan takip isteği geri çekildi.")
    except Exception as e:
        print(f"{username} işlemi sırasında bir hata oluştu: {e}")

# Tarayıcıyı kapat
driver.quit()
