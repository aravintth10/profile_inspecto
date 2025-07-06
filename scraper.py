from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
from utils import save_json

def init_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

def scrape_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(5)

    name = driver.find_element(By.CSS_SELECTOR, "h1").text
    headline = driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words").text
    about = ""
    try:
        about = driver.find_element(By.ID, "about").text
    except:
        pass

    experience = []
    try:
        blocks = driver.find_elements(By.CSS_SELECTOR, "#experience + div li")
        for b in blocks:
            experience.append(b.text)
    except:
        pass

    data = {
        "name": name,
        "headline": headline,
        "about": about,
        "experience": experience
    }

    save_json(data, "profiles/raw_profile.json")
    print("✅ Profile saved.")
    return data

if __name__ == "__main__":
    driver = init_driver()
    login(driver)
    url = input("Paste LinkedIn profile URL: ")
    scrape_profile(driver, url)
    driver.quit()
