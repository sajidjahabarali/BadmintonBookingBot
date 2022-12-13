from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


def log_in():
    attempt = 1
    while (attempt <= 3):
        try:
            time.sleep(3)
            driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
            driver.find_element(By.NAME, 'username').send_keys(
                os.getenv('BETTER_GYM_EMAIL_ADDRESS'))
            driver.find_element(By.NAME, 'password').send_keys(
                os.getenv('BETTER_GYM_PASSWORD'))

            time.sleep(3)
            driver.find_element(
                By.XPATH, '//button[@data-testid="log-in"]').click()
            break
        except NoSuchElementException:
            if attempt == 3:
                raise Exception('Maximum retries exceeded')
            else:
                attempt += 1
    return


def add_time_slot_to_basket(time_slot):
    attempt = 1
    while (attempt <= 3):
        print('attempt ', attempt)
        time.sleep(3)
        rows = driver.find_elements(By.CLASS_NAME, 'jtkyDd')
        for row in rows:
            # print(row.find_element(By.CLASS_NAME, 'kOypzl').text, '|', time_slot)
            if (row.find_element(By.CLASS_NAME, 'kOypzl').text == time_slot):
                row.find_element(By.CLASS_NAME, 'bGmnCq').click()
                time.sleep(3)
                driver.find_element(By.CLASS_NAME, 'fa-chevron-down').click()
                for x in range(0, 4):
                    if (driver.find_element(
                            By.CSS_SELECTOR, '[id$=option-' + str(x) + ']').text[:4] != 'FULL'):
                        driver.find_element(
                            By.CSS_SELECTOR, '[id$=option-' + str(x) + ']').click()
                        break
                time.sleep(3)
                row.find_element(
                    By.XPATH, '//span[text()="Add to basket"]').click()
                time.sleep(3)
                return
        attempt += 1

    return


def checkout():
    driver.find_element(By.XPATH, '//span[text()="Checkout now"]').click()
    time.sleep(3)
    driver.find_element(By.NAME, 'billingFirstName').send_keys(
        os.getenv('BILLING_FIRST_NAME'))
    driver.find_element(By.NAME, 'billingLastName').send_keys(
        os.getenv('BILLING_LAST_NAME'))
    driver.find_element(By.NAME, 'billingAddressLineOne').send_keys(
        os.getenv('BILLING_ADDRESS_LINE_ONE'))
    driver.find_element(By.NAME, 'billingCity').send_keys(
        os.getenv('BILLING_CITY'))
    driver.find_element(By.NAME, 'billingPostcode').send_keys(
        os.getenv('BILLING_POSTCODE'))
    driver.find_element(By.NAME, 'cardholderName').send_keys(
        os.getenv('CARDHOLDER_NAME'))
    driver.find_element(By.NAME, 'cardNumber').send_keys(
        os.getenv('CARD_NUMBER'))
    driver.find_element(By.NAME, 'expiryDate').send_keys(
        os.getenv('EXPIRY_DATE'))
    driver.find_element(By.NAME, 'securityCode').send_keys(
        os.getenv('SECURITY_CODE'))
    driver.find_element(By.XPATH, '//span[contains(text(), "Pay")]').click()


os.environ['BETTER_GYM_EMAIL_ADDRESS'] = 'email'
os.environ['BETTER_GYM_PASSWORD'] = 'password'
os.environ['BILLING_FIRST_NAME'] = 'name'
os.environ['BILLING_LAST_NAME'] = 'last name'
os.environ['BILLING_ADDRESS_LINE_ONE'] = '123 Test Road'
os.environ['BILLING_CITY'] = 'London'
os.environ['BILLING_POSTCODE'] = 'AB1 2CD'
os.environ['CARDHOLDER_NAME'] = 'name'
os.environ['CARD_NUMBER'] = '1234567890123456'
os.environ['EXPIRY_DATE'] = '12/30'
os.environ['SECURITY_CODE'] = '123'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.delete_all_cookies()
driver.get(
    'https://bookings.better.org.uk/location/hendon-leisure-centre/badminton-60min/2022-12-16/by-time/')


log_in()
add_time_slot_to_basket('13:00 - 14:00')
add_time_slot_to_basket('14:00 - 15:00')
checkout()

# while (attempt < 3):
#     try:
#         time.sleep(3)
#         driver.find_element(By.XPATH, '//span[text()="Add to basket"]').click()
#         driver.find_element(By.NAME, 'username').send_keys(
#             os.getenv('BETTER_GYM_EMAIL_ADDRESS'))
#         driver.find_element(By.NAME, 'password').send_keys(
#             os.getenv('BETTER_GYM_PASSWORD'))

#         time.sleep(3)
#         driver.find_element(
#             By.XPATH, '//button[@data-testid="log-in"]').click()
#         break
#     except NoSuchElementException:
#         if attempt == 3:
#             raise Exception('Maximum retries exceeded')


def click_after_button_loads():
    delay = 10
    try:
        WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((
                By.XPATH, '//span[text()="Add to basket"]'))).click()
    except TimeoutException:
        print("Loading took too much time!")
