import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        print("Odpiram Wise Timetable...")
        driver.get("https://wise-tt.com/wtt_um_feri/")
        wait = WebDriverWait(driver, 30)
        
        # 1. Najprej kliknemo na prvi dropdown (tisti oranžni na tvoji sliki)
        print("Odpiram dropdown meni za Program...")
        # Iščemo puščico prvega dropdowna
        dropdown_arrow = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-selectonemenu-trigger")))
        dropdown_arrow.click()
        time.sleep(2)
        
        # 2. Zdaj ko je meni odprt, poiščemo tvoj program
        print("Iščem: RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)")
        # Uporabimo XPATH, ki najde 'li' element (seznam), ki vsebuje tvoj program
        program_xpath = "//li[contains(text(), 'RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)')]"
        program_item = wait.until(EC.presence_of_element_located((By.XPATH, program_xpath)))
        
        # Ker je seznam morda dolg, Seleniumu rečemo, naj se "skrola" do njega
        driver.execute_script("arguments[0].scrollIntoView(true);", program_item)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", program_item)
        print("Program izbran!")
        
        time.sleep(5) # Čakamo, da se tabela osveži
        
        # 3. Klik na iCal-vse
        print("Klikam iCal-vse...")
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'iCal-vse')]")))
        driver.execute_script("arguments[0].click();", ical_btn)
        
        print("Čakam na prenos...")
        time.sleep(15)
        
        # 4. Preveri datoteko
        files = os.listdir(download_path)
        for file in files:
            if file.endswith(".ics"):
                if os.path.exists("urnik.ics"): os.remove("urnik.ics")
                os.rename(os.path.join(download_path, file), "urnik.ics")
                print("ZMAGA!")
                return True
        
        return False

    except Exception as e:
        print(f"Napaka: {e}")
        driver.save_screenshot("dropdown_error.png")
        with open("urnik.ics", "w") as f: f.write(f"Napaka: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
