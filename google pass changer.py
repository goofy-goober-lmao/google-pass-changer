import random
import string
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(filename='password_change.log', level=logging.INFO)


def generate_password(length=25):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def change_password(browser, email):
    try:
        browser.get('https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.co.uk%2F&ec=GAZAmgQ&hl=en&passive=true&ifkv=ATuJsjzp1D0Joht5NICMcjyAAhOsFD7xWhgKXe0braDNp_UItO1QR0q9OMYoV2tISrlR2r70gn8hsA&theme=glif&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

        print("Writing email...")
        browser.find_element(By.ID, 'identifierId').send_keys(email)
        print("Successfully Written Email...")

        print("Verifying email...")
        browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').click()

        password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

        print("Writing Password...")
        browser.find_element(By.CSS_SELECTOR, password_selector).send_keys("GSAstudent12345")  # CHANGE PASSWORD ACCORDINGLY ###########################################################################################
        browser.find_element(By.CSS_SELECTOR, '#passwordNext > div > button > span').click()
        print("Attempting to log in...")

        # Check for cookies dialog
        try:
            WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#L2AGLb')))
            browser.find_element(By.CSS_SELECTOR, '#L2AGLb').click()
            print("Accepted cookies.")
        except TimeoutException:
            print("No cookies found, proceeding...")
        time.sleep(1)
        browser.get('https://myaccount.google.com/signinoptions/password')
        print("Generating New Password...")

        new_password =  generate_password()  # MAKE SURE TO REMOVE "TheEvent1!" AND THE '#' BEFORE generate_password() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print("Generated New Password:", new_password)
        print("Changing Password...")
        new_pass_one = "#i5"
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, new_pass_one)))

        print("Writing New Password...")
        browser.find_element(By.CSS_SELECTOR, new_pass_one).send_keys(new_password)

        print("Successfully Written New Password...")
        new_pass_two = "#i11"
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, new_pass_two)))

        print("Confirming New Password...")
        browser.find_element(By.CSS_SELECTOR, new_pass_two).send_keys(new_password)
        print("Successfully Written New Password...")

        print("Authorising...")
        browser.find_element(By.CSS_SELECTOR, '#yDmH0d > c-wiz > div > div:nth-child(2) > div:nth-child(2) > c-wiz > div > div.VfPpkd-WsjYwc.VfPpkd-WsjYwc-OWXEXe-INsAgc.KC1dQ.Usd1Ac.AaN0Dd.F2KCCe.Z2xVec.E2bpG.injfOc > form > div > div.GFJYae.lY6Rwe > div > div > button > span.UywwFc-vQzf8d').click()

        print("Confirm for all devices...")
        change_password_header = "#yDmH0d > div.bwApif-Sx9Kwc.bwApif-Sx9Kwc-OWXEXe-n2to0e.iteLLc.bwApif-Sx9Kwc-OWXEXe-FNFY6c > div.bwApif-wzTsW > div > div.bwApif-T0kwCb > div:nth-child(2) > button"
        try:  # click the confirm
            WebDriverWait(browser, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, change_password_header))).click()
            print("Clicked on 'Change password' header...")
        except TimeoutException:
            print("Element not found or not visible within the specified time.")
        except Exception as E:
            print(f"Error clicking on 'Change password' header: {str(E)}")
        time.sleep(1)
        print("Success! Saved to newaccounts.txt")

        with open('newaccounts.txt', 'a') as FILE:
            FILE.write(f"Email: {email}, New Password: {new_password}\n")

        # sign out
        browser.get("https://accounts.google.com/SignOutOptions?hl=en-GB&continue=https://myaccount.google.com/%3Futm_source%3Dsign_in_no_continue%26pli%3D1%26nlr%3D1%26pageId%3Dnone&ec=GBRAwAE")
        signout = '#signout'
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, signout)))
        browser.find_element(By.CSS_SELECTOR, signout).click()
        time.sleep(1)
        return new_password  # loop

    except NoSuchElementException:
        logging.error(f"Failed to change password for {email}: Element not found")
        with open('newaccounts.txt', 'a') as FILE:
            FILE.write(f"Failed Login Email: {email}\n")
        return None

    except Exception as E:
        logging.error(f"Failed to change password for {email}: {str(E)}")
        with open('newaccounts.txt', 'a') as FILE:
            FILE.write(f"Failed Login Email: {email}\n")
        return None


if __name__ == "__main__":
    try:
        options = webdriver.ChromeOptions()
        browser_width = 1052
        browser_height = 864
        browser_position_x = 0
        browser_position_y = 0
        options.add_argument(f"--window-size={browser_width},{browser_height}")
        options.add_argument(f"--window-position={browser_position_x},{browser_position_y}")

        browser = webdriver.Chrome(options=options)

        usernames_file = 'usernames.txt'
        new_accounts_file = 'newaccounts.txt'

        with open(usernames_file, 'r') as file:
            usernames = [username.strip() for username in file.readlines()]

        with open(new_accounts_file, 'w') as file:
            for username in usernames:
                email = f"{username}@george-spencer.notts.sch.uk"  # CHANGE EMAIL ADDRESS ACCORDINGLY ###########################################################################################
                print(f"Changing password for {email}...")

                new_password = change_password(browser, email)
                if new_password:
                    logging.info(f"Password changed for {email}")
                else:
                    logging.error(f"Failed to change password for {email}")

        time.sleep(100)
        browser.quit()

    except Exception as e:
        logging.error("An error occurred: " + str(e))
