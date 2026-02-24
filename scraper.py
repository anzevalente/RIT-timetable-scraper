import requests

# Glavna stran in link za prenos
BASE_URL = "https://wise-tt.com/wtt_um_feri/"
# Uporabila bova ID 46, ki si ga našel z Inspect Element
DOWNLOAD_URL = "https://wise-tt.com/wtt_um_feri/rest/ical/v2/group/46"

def download():
    # Ustvarimo sejo, ki si zapomni piškotke (cookies)
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': BASE_URL
    }

    try:
        # 1. korak: Obiščemo glavno stran, da dobimo piškotke
        print("Obiskujem glavno stran...")
        session.get(BASE_URL, headers=headers)

        # 2. korak: Poskusimo prenesti urnik z isto sejo
        print(f"Poskušam prenesti urnik iz: {DOWNLOAD_URL}")
        r = session.get(DOWNLOAD_URL, headers=headers)

        if r.status_code == 200 and len(r.content) > 100:
            with open("urnik.ics", "wb") as f:
                f.write(r.content)
            print("ZMAGA! Urnik je prenesen.")
        else:
            print(f"Napaka! Status: {r.status_code}. Dolžina vsebine: {len(r.content)}")
            # Če dobimo prazno datoteko ali 404, izpišemo vsebino za debug
            print("Odziv strežnika:", r.text[:100])
            
    except Exception as e:
        print(f"Kritična napaka: {e}")

if __name__ == "__main__":
    download()
