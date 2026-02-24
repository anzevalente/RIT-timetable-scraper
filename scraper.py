import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_urnik():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    download_path = os.getcwd()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://wise-tt.com/wtt_um_feri/")
        wait = WebDriverWait(driver, 25)
        
        # 1. Iskanje programa - uporabila bova blažji filter
        print("Iščem program...")
        program_xpath = "//td[contains(text(), 'RAČUNALNIŠTVO') and contains(text(), 'BV20')]"
        program_btn = wait.until(EC.element_to_be_clickable((By.XPATH, program_xpath)))
        program_btn.click()
        print("Program kliknjen.")
        
        time.sleep(5) # Počakamo na AJAX
        
        # SLIKAJ ZASLON (za vsak slučaj, da vidiva kaj se dogaja)
        driver.save_screenshot("debug_screen.png")

        # 2. Iskanje gumba iCal-vse
        print("Iščem gumb iCal-vse...")
        # Včasih je gumb v bistvu 'span' znotraj gumba, zato iščeva po tekstu kjerkoli
        ical_xpath = "//*[contains(text(), 'iCal-vse')]"
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ical_xpath)))
        ical_btn.click()
        print("Gumb kliknjen.")
        
        time.sleep(15) # Čas za prenos
        
        files = os.listdir(download_path)
        for file in files:
            if file.endswith(".ics"):
                os.rename(os.path.join(download_path, file), "urnik.ics")
                print("USPEH!")
                return True
        
        print("Ni bilo .ics datoteke.")
        return False

    except Exception as e:
        print(f"Napaka: {e}")
        driver.save_screenshot("error_screen.png")
        with open("urnik.ics", "w") as f: f.write(f"Napaka: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
