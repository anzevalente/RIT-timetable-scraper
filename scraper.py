import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fix_ical_content(filepath):
    """Funkcija, ki združi podatke v pregleden naslov: PREDMET | TIP | PROFESOR | PROSTOR"""
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    current_summary = ""
    summary_index = -1
    
    for line in lines:
        if line.startswith("SUMMARY:"):
            current_summary = line.replace("SUMMARY:", "").strip()
            new_lines.append(line)
            summary_index = len(new_lines) - 1
            
        elif line.startswith("DESCRIPTION:") and summary_index != -1:
            description = line.replace("DESCRIPTION:", "").strip()
            # Očistimo opis in zamenjamo vejice/nove vrstice z navpičnico
            # Wise-tt v opisu običajno ločuje podatke z \n
            details = description.replace("\\n", " | ").replace("\\t", " ").strip()
            
            # Sestavimo nov naslov: IME PREDMETA | OSTALI PODATKI
            new_summary = f"SUMMARY:{current_summary} | {details}\r\n"
            new_lines[summary_index] = new_summary
            new_lines.append(line)
            summary_index = -1 # Resetiramo za naslednji dogodek
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# --- OSTALI DEL KODE OSTANE ISTI KOT PREJ ---

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
        
        dropdown_arrow = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-selectonemenu-trigger")))
        dropdown_arrow.click()
        time.sleep(2)
        
        program_xpath = "//li[contains(text(), 'RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE VS (BV20)')]"
        program_item = wait.until(EC.presence_of_element_located((By.XPATH, program_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", program_item)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", program_item)
        
        time.sleep(5)
        
        ical_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'iCal-vse')]")))
        driver.execute_script("arguments[0].click();", ical_btn)
        
        time.sleep(15)
        
        for file in os.listdir(download_path):
            if file.endswith(".ics"):
                target = "urnik.ics"
                if os.path.exists(target): os.remove(target)
                os.rename(os.path.join(download_path, file), target)
                fix_ical_content(target)
                print("Urnik uspesno posodobljen z lepsimi naslovi!")
                return True
        return False
    except Exception as e:
        print(f"Napaka: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    download_urnik()
