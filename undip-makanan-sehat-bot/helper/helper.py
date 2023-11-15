import sys
import locale
import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


class FoodTruckHelper:

    locale.setlocale(locale.LC_TIME, 'id_ID')
    
    options = Options()
    options.add_experimental_option('detach',True)
    options.add_argument('--disable-notifications') 
    
    # # Using local chrome driver
    # import os
    # os.environ['PATH'] += r"../Driver"
    # driver = webdriver.Chrome(options=options)

    # Using webdriver-manager (recommended)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    location = ['S', 'H', 'Auditorium F', 'Auditorium I']
    date = datetime.today().strftime('X%d %B %Y').replace('X0','X').replace('X','')

    def __init__(self, email, pw, locIndex, delay, interval):  
        self.email = email  
        self.pw = pw
        self.locIndex = locIndex - 1
        self.delay = delay
        self.interval = interval
    

    def login(self):
        self.printColor('yellow','[SYS] Logging in...')
        driver = self.driver
        try:
            driver.get('https://sso.undip.ac.id/auth/user/login')

            loginForm = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, 'identity'))
            )
            loginForm.send_keys(self.email + Keys.ENTER)

            pwForm = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'form-control.input.ext-input.text-box.ext-text-box'))
            )
            pwForm.send_keys(self.pw + Keys.ENTER)
            
            try:
                if WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID,'passwordError'))
                ):
                    self.printColor('red','[ERROR] Incorrect password')
                    driver.quit()
                    sys.exit(1)
            except Exception:
                pass

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'brand-text'))
            )

            self.printColor('green','[SYS] Login successful!')
        except Exception as e:
            self.printColor('red','[ERROR] Login failed')
            print(e)
            self.terminate()
    

    def navigate(self):
        self.printColor('yellow','[SYS] Navigating to form page...')
        driver = self.driver
        try:
            driver.get('https://form.undip.ac.id/sso/auth?t=MTY4NDA1MDYwNg==')

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'content-header-title.mb-0.d-inline-block.font-weight-bold'))
            )

            driver.get('https://form.undip.ac.id/makanansehat/pendaftaran')

            self.printColor('green','[SYS] Arrived in form page')
        except Exception as e:
            self.printColor('red','[ERROR] Failed to navigate to the form page')
            print(e)
            self.terminate()


    def getCoupon(self):
        self.printColor('yellow','[SYS] Attempting to get coupon...')
        driver = self.driver

        selection = f"{self.date} - Lokasi {self.location[self.locIndex]}"

        targetTime = datetime.now().replace(hour=10, minute=0, second=0)
        currentTime = datetime.now()

        waitTime = (targetTime - currentTime).total_seconds() + self.delay

        if (waitTime > 0):
            self.printColor('yellow',f'[SYS] Waiting for {waitTime} seconds until 10:00 WIB, do not close the browser')
            time.sleep(waitTime)
        else:
            self.printColor('yellow','[SYS] It is currently past 10:00 WIB, trying anyway...')
        
        try:
            driver.refresh()

            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-square.btn-indigo'))
            )

            select = Select(driver.find_element(By.ID,'tanggal'))

            # Only iterate through the last 5 items in the options list
            for option in select.options[-5:]:
                if selection in option.text:
                    option.click()
                    print(option.text)
                    break

            saveButton = driver.find_element(By.CLASS_NAME,'btn.btn-square.btn-indigo')
            saveButton.click()

            WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )
            Alert(driver).accept()

        except Exception as e:
            self.printColor('yellow','Sorry, unable to obtain coupon, terminating program...')
            # self.terminate()

    
    def GetCouponSentry(self):
        self.printColor('yellow',f'[SYS] Sentry mode: interval {self.interval}s')
        driver = self.driver

        selection = f"{self.date} - Lokasi {self.location[self.locIndex]}"
        selected = False
        
        while not selected:
            self.printColor('yellow','[SYS] Refreshing...')
            try:
                driver.refresh()

                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-square.btn-indigo'))
                )

                select = Select(driver.find_element(By.ID,'tanggal'))

                # Only iterate through the last 5 items in the options list
                for option in select.options[-5:]:
                    if selection in option.text:
                        option.click()
                        print(option.text)
                        selected = True
                        break

                if not selected:
                    self.printColor('yellow','[SYS] No coupon found')
                    time.sleep(self.interval)
            except Exception as e:
                pass
            
        
        self.printColor('green',f'[SYS] Coupon found!')
        try:
            saveButton = driver.find_element(By.CLASS_NAME,'btn.btn-square.btn-indigo')
            saveButton.click()

            WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )
            Alert(driver).accept()
        except Exception as e:
            self.printColor('yellow','Sorry, unable to obtain coupon, terminating program...')
            # self.terminate()

    
    def getCouponTest(self):
        self.printColor('yellow','[SYS] Attempting to get coupon...')
        driver = self.driver
        try:
            driver.refresh()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-square.btn-indigo'))
            )

            select = Select(driver.find_element(By.ID,"tanggal"))

            for option in select.options[-1:]:
                option.click()
                print(option.text)
                break

            saveButton = driver.find_element(By.CLASS_NAME,'btn.btn-square.btn-indigo')
            saveButton.click()

            WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )

            Alert(driver).accept()

            self.printColor('green','[SYS] Test successful!')
            driver.quit()
            sys.exit(1)
        except Exception as e:
            self.printColor('red',f'[ERROR] Test failed')
            print(e)
            self.terminate()
    

    def getScreenshot(self):
        driver = self.driver

        locF = ['SC', 'SAM-WA', 'FPIK', 'Imam Bardjo']

        dateF = datetime.today().strftime('%Y-%m-%d')
        filename = f"{dateF} {locF[self.locIndex-1]} {self.email[:self.email.find('@')]}.png"
        # 9999-99-99 SC john.png

        try:
            driver.get('https://form.undip.ac.id/makanansehat/pendaftaran/riwayat')

            coupon = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[id*=kupon_makanansehat_]'))
            )

            couponImg = coupon.screenshot_as_png
            with open(filename, 'wb') as f:
                f.write(couponImg)
            
            print(f"[SYS] Coupon saved as {filename}")
        except Exception as e:
            print(f'[ERROR] Unable to save coupon as image \n{e}')
            self.terminate()

    
    def terminate(self):
        self.driver.quit()
        sys.exit(1)


    def printColor(self, col, txt):
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m'
        }
        print(f'{colors[col]}{txt}\033[0m')
        