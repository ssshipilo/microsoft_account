import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random
import string
import json 
import os
import bs4
import uuid
import names

class Microsoft():

    def __init__(self) -> None:
        self.chrome_driver = "./browser/chromedriver.exe"

    def createAccount(self):
        def generate_name():
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            return [first_name, last_name]

        def generate_password():
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            numbers = string.digits
            special_characters = '!@#$%^&*(),.?":{}|<>'

            password = [
                random.choice(lowercase),
                random.choice(uppercase),
                random.choice(numbers),
                random.choice(special_characters)
            ]

            for i in range(4, 8):
                password.append(random.choice(lowercase + uppercase + numbers + special_characters))

            random.shuffle(password)
            return ''.join(password)

        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+'
        random_char = random.choice(characters)
        service = Service(self.chrome_driver)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")
        options.add_argument("--lang=ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
        options.add_argument("--remote-debugging-port=9223")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://signup.live.com/signup')

        input_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="MemberName"]'))
        )
        name = generate_name()
        email = str(uuid.uuid1()).replace('-', '')
        new_email = name[0] + email + "@outlook.com"
        input_email.send_keys(new_email)
        
        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="iSignupAction"]'))
        )
        submit.click()

        # Create password
        while True:
            try:
                password = generate_password()
                input_password = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="PasswordInput"]'))
                )
                input_password.send_keys(password)
                break
            except:
                continue

        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="iSignupAction"]'))
        )
        submit_btn.click()

        time.sleep(1)
        first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="FirstName"]'))
        )
        first_name.send_keys(name[0])

        last_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="LastName"]'))
        )
        last_name.send_keys(name[1])

        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="iSignupAction"]'))
        )
        submit_btn.click()

        BirthDay_day = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="BirthDay"]'))
        )
        select = Select(BirthDay_day)
        select.select_by_visible_text('18')

        BirthDay_mouth = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="BirthMonth"]'))
        )
        BirthDay_mouth.click()
        BirthDay_mouth = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="BirthMonth"]/option[4]'))
        )
        BirthDay_mouth.click()

        BirthDay_year = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="BirthYear"]'))
        )
        BirthDay_year.send_keys("1996")

        check_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="iSignupAction"]'))
        )
        check_box.click()

        # Captcha
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="enforcementFrame"]'))
        )
        driver.switch_to.frame(iframe)
        iframe_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="arkose"]/div/iframe'))
        )
        driver.switch_to.frame(iframe_content)
        iframe_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="game-core-frame"]'))
        )
        driver.switch_to.frame(iframe_content)
        while True:
            try:
                next_to_iamge = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/button'))
                )
                next_to_iamge.click()
                break
            except:
                continue
            
        time.sleep(5)
        while True:
            try:
                image_capcha = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]'))
                )   
                image_capcha.screenshot("image_before_switch.png")
                break
            except:
                continue

        # Signing up a new account
        data_file = './microsoft_user.json'
        if not os.path.exists(data_file):
            with open(data_file, 'w') as f:
                json.dump([], f)
        with open(data_file, 'r') as f:
            data = json.load(f)
        data.append({'login': new_email, "password": password})
        with open(data_file, 'w') as f:
            json.dump(data, f)

        time.sleep(50000)

if __name__ == "__main__":
    px = Microsoft()
    px.createAccount()