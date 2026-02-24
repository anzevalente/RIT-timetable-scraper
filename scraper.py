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
    
    # Nastavitev mape za prenos
    download_path = os.getcwd()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Odpiram Wise Timetable...")
        driver.get("https://wise-tt.com/wtt_um_feri/")
        wait = WebDriverWait(driver, 30)
        
        # 1. Klik na program
        print("Iščem program: RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)")
        # Ta XPath najde tabelo (td), ki vsebuje točno to besedilo
        program_xpath = "//td[contains(text(), 'RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)')]"
        program_btn = wait.until(EC.element_to_be_clickable((By.XPATH, program_xpath)))
        
        driver.execute_script("arguments[0].scrollIntoView();", program_btn)
        time.sleep(2)
        program_btn.click()
        print("Program izbran!")
        
        # Počakamo, da se AJAX urnik naloži
        time.sleep(5)
        
        # 2. Klik na gumb iCal-vse
        print("Iščem gumb: iCal-vse")
        # Iščemo gumb, ki ima v sebi besedilo 'iCal-vse'
        ical_xpath = "//button[contains(., 'iCal-vse')]"
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ical_xpath)))
        
        driver.execute_script("arguments[0].scrollIntoView();", ical_btn)
        time.sleep(2)
        ical_btn.click()
        print("Gumb iCal-vse kliknjen! Čakam na prenos...")
        
        # Počakamo na prenos (na GitHubu lahko traja malo dlje)
        time.sleep(15)
        
        # 3. Preimenovanje datoteke
        files = os.listdir(download_path)
        print(f"Najdene datoteke v mapi: {files}")
        
        for file in files:
            if file.endswith(".ics"):
                old_path = os.path.join(download_path, file)
                new_path = os.path.join(download_path, "urnik.ics")
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                print(f"USPEH: Datoteka {file} je zdaj urnik.ics")
                return True
                
        print("NAPAKA: Nobena .ics datoteka ni bila prenesena.")
        return False

    except Exception as e:
        print(f"Napaka: {e}")
        # Ustvarimo datoteko, da preprečimo exit code 128
        with open("urnik.ics", "w") as f: f.write("error")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
