import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import allure

# Constants
LOGIN_URL = "https://magento.softwaretestingboard.com/customer/account/login/"
ACCOUNT_URL = "https://magento.softwaretestingboard.com/customer/account/"
EMAIL_URL = "rima.rima.1@yandex.ru"
PASSWORD = "RimaQA2024/"
NEW_PASSWORD = "RimaQA2024/"


@pytest.fixture(scope="module")
def driver():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.regression
@allure.feature('Login Tests')
@allure.suite('User Authentication')
@allure.title('Invalid Login Test')
@allure.description('This test verifies that login fails with invalid credentials.')
@allure.severity('critical')
def test_invalid_login(driver):
    with allure.step('Navigate to the login page'):
        driver.get(LOGIN_URL)
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("invalidemail@gmail.com")
    with allure.step('Enter invalid credentials'):
        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys("invalidpassword")
    with allure.step('Attempt to login'):
        login_button = driver.find_element(By.ID, "send2")
        login_button.click()

    time.sleep(3)
    with allure.step('Verify the error message'):
        error_message = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div[2]/div/div/div')
        assert "Please wait and try again later." in error_message.text


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('Login Tests')
@allure.suite('User Authentication')
@allure.title('Valid Login Test')
@allure.description('This test verifies that login succeeds with valid credentials.')
@allure.severity('critical')
def test_login(driver):
    with allure.step('Navigate to the login page'):
        driver.get(LOGIN_URL)

    with allure.step('Enter valid credentials'):
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(EMAIL_URL)

    with allure.step('Enter password'):
        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(PASSWORD)

    with allure.step('Attempt to login'):
        login_button = driver.find_element(By.ID, "send2")
        login_button.click()

    time.sleep(3)
    with allure.step('Verify successful login'):
        assert driver.current_url == ACCOUNT_URL


@pytest.mark.regression
@allure.feature('Password Management')
@allure.suite('Account Settings')
@allure.title('Incorrect Current Password Test')
@allure.description('This test verifies that attempting to change password with an incorrect current password fails.')
@allure.severity('critical')
def test_change_password_incorrect_current(driver):
    with allure.step('Navigate to the account page'):
        driver.get(ACCOUNT_URL)
        change_password_link = driver.find_element(By.CSS_SELECTOR, ".action.change-password")
        change_password_link.click()

    with allure.step('Enter incorrect current password'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys("incorrectpassword")

    with allure.step('Enter new password'):
        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Confirm new password'):
        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Attempt to save changes'):
        save_button = driver.find_element(By.XPATH, '//*[@id="form-validate"]/div/div[1]/button')
        save_button.click()

    time.sleep(3)
    with allure.step('Verify error message'):
        error_message = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[1]/div[2]/div/div/div')
        assert "The password doesn't match this account" in error_message.text


@pytest.mark.regression
@allure.feature('Password Management')
@allure.suite('Account Settings')
@allure.title('Password Mismatch Test')
@allure.description('This test verifies that changing password fails when confirmation password does not match.')
@allure.severity('critical')
def test_change_password_mismatch(driver):
    with allure.step('Navigate to the account page'):
        driver.get(ACCOUNT_URL)
    with allure.step('Open change password form'):
        change_password_link = driver.find_element(By.CSS_SELECTOR, ".action.change-password")
        change_password_link.click()

    with allure.step('Enter current password'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys(PASSWORD)

    with allure.step('Enter new password'):
        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Enter mismatched confirmation password'):
        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys("mismatchedpassword")

    with allure.step('Attempt to save changes'):
        save_button = driver.find_element(By.XPATH, '//*[@id="form-validate"]/div/div[1]/button')
        save_button.click()

    time.sleep(3)
    with allure.step('Verify error message'):
        error_message = driver.find_element(By.ID, "password-confirmation-error")
        assert "Please enter the same value again." in error_message.text


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('Password Management')
@allure.suite('Account Settings')
@allure.title('Successful Password Change Test')
@allure.description('This test verifies that a user can successfully change their password.')
@allure.severity('critical')
def test_change_password(driver):
    with allure.step('Navigate to the account page'):
        driver.get(ACCOUNT_URL)

    with allure.step('Open change password form'):
        change_password_link = driver.find_element(By.CSS_SELECTOR, ".action.change-password")
        change_password_link.click()

    with allure.step('Enter current password'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys(PASSWORD)

    with allure.step('Enter new password'):
        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Confirm new password'):
        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Attempt to save changes'):
        save_button = driver.find_element(By.XPATH, '//*[@id="form-validate"]/div/div[1]/button')
        save_button.click()

    with allure.step('Verify success message'):
        success_message = driver.find_element(By.XPATH, "//div[contains(@class, 'message-success')]")
        assert "You saved the account information." in success_message.text