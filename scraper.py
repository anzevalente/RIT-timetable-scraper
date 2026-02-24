import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fix_ical_content(filepath):
    """Funkcija, ki premakne podrobnosti iz opisa v naslov dogodka."""
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    current_summary = ""
    
    for i in range(len(lines)):
        line = lines[i]
        
        # Najdemo naslov (SUMMARY)
        if line.startswith("SUMMARY:"):
            current_summary = line.replace("SUMMARY:", "").strip()
            new_lines.append(line) # Začasno dodamo, popravili bomo ko pridemo do opisa
            summary_index = len(new_lines) - 1
            
        # Najdemo opis (DESCRIPTION), kjer se skrivajo profesor, prostor itd.
        elif line.startswith("DESCRIPTION:") and current_summary:
            description = line.replace("DESCRIPTION:", "").strip()
            # Očistimo opis čudnih znakov (\n, \t)
            clean_info = description.replace("\\n", ", ").replace("\\t", " ").strip()
            
            # Sestavimo nov, bogat naslov: Predmet, Tip, Profesor, Učilnica
            # Outlook bo zdaj prikazal vse to hkrati
            new_summary = f"SUMMARY:{current_summary}, {clean_info}\r\n"
            new_lines[summary_index] = new_summary
            new_lines.append(line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

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
        wait = WebDriverWait(driver, 30)
        
        # 1. Klik na dropdown in izbira programa
        dropdown_arrow = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-selectonemenu-trigger")))
        dropdown_arrow.click()
        time.sleep(2)
        
        program_xpath = "//li[contains(text(), 'RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)')]"
        program_item = wait.until(EC.presence_of_element_located((By.XPATH, program_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", program_item)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", program_item)
        
        time.sleep(5)
        
        # 2. Klik na iCal-vse
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'iCal-vse')]")))
        driver.execute_script("arguments[0].click();", ical_btn)
        
        time.sleep(15)
        
        # 3. Obdelava datoteke
        for file in os.listdir(download_path):
            if file.endswith(".ics"):
                target = "urnik.ics"
                if os.path.exists(target): os.remove(target)
                os.rename(os.path.join(download_path, file), target)
                
                # KLJUČNI KORAK: Popravi vsebino, da bo več informacij v naslovu
                fix_ical_content(target)
                print("Urnik uspešno prenesen in obdelan!")
                return True
        return False
    except Exception as e:
        print(f"Napaka: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
