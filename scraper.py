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
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Odpiram stran Wise Timetable...")
        driver.get("https://wise-tt.com/wtt_um_feri/")
        wait = WebDriverWait(driver, 20)
        
        # 1. Klik na program RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE
        print("Iščem in klikam na program...")
        # Iskanje elementa, ki vsebuje točno to besedilo
        program_xpath = "//td[contains(text(), 'RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE')]"
        program_btn = wait.until(EC.element_to_be_clickable((By.XPATH, program_xpath)))
        program_btn.click()
        
        # Počakamo trenutek, da se urnik naloži (AJAX)
        time.sleep(3)
        
        # 2. Klik na gumb iCal-vse
        # Ker gumbi na Wise-TT pogosto nimajo ID-ja, ga poiščeva po besedilu na gumbu
        print("Iščem gumb iCal-vse...")
        ical_xpath = "//button[contains(., 'iCal-vse')]"
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ical_xpath)))
        ical_btn.click()
        
        print("Kliknjeno! Čakam na prenos...")
        time.sleep(10) # Dovolj časa za prenos v oblaku
        
        # 3. Preveri datoteke v mapi
        files = os.listdir(download_path)
        print(f"Datoteke v mapi: {files}")
        
        for file in files:
            if file.endswith(".ics"):
                old_path = os.path.join(download_path, file)
                new_path = os.path.join(download_path, "urnik.ics")
                # Če urnik.ics že obstaja, ga pobrišemo
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                print(f"USPEH: Datoteka {file} preimenovana v urnik.ics")
                return True
                
        print("NAPAKA: Nobena .ics datoteka ni bila najdena.")
        # Ustvarimo nujno datoteko, da Actions ne padejo
        with open("urnik.ics", "w") as f: f.write("Prazno")
        return False

    except Exception as e:
        print(f"Prišlo je do napake: {e}")
        with open("urnik.ics", "w") as f: f.write(f"Error: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
