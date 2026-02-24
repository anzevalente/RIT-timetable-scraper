import requests

# Prepričaj se, da je link točno tak (brez presledkov na koncu)
URL = "https://wise-tt.com/wtt_um_feri/rest/ical/v2/group/RIT_VS_1"

def download():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(URL, headers=headers)
        if r.status_code == 200:
            # Ta vrstica ustvari datoteko
            with open("urnik.ics", "wb") as f:
                f.write(r.content)
            print("Urnik uspesno prenesen in shranjen v urnik.ics!")
        else:
            print(f"Napaka na strezniku: {r.status_code}")
    except Exception as e:
        print(f"Prislo je do napake: {e}")

if __name__ == "__main__":
    download()
