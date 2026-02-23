import requests
from bs4 import BeautifulSoup

print("--- PriceScout Mobile: Spouštím průzkumníka ---")

# 1. Adresa, kterou chceme prozkoumat (Bazoš - Mobily)
url = "https://mobil.bazos.cz/"

# 2. Maskování (tváříme se jako běžný prohlížeč Chrome, ne jako robot)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # 3. Stažení webové stránky
    print("Stahuji data z webu...")
    odpoved = requests.get(url, headers=headers)
    odpoved.raise_for_status() # Zkontroluje, jestli server nehodil chybu (např. 404)

    # 4. Předání HTML kódu do BeautifulSoup
    soup = BeautifulSoup(odpoved.text, 'lxml')

    # 5. Hledání inzerátů (Bazoš obvykle používá třídu 'inzeraty')
    inzeraty = soup.find_all('div', class_='inzeraty')

    print(f"Nalezeno {len(inzeraty)} inzerátů na první stránce.\n")

    # 6. Projdeme prvních 5 inzerátů a vypíšeme je
    for inzerat in inzeraty[:5]:
        # Najdeme nadpis
        nadpis_element = inzerat.find('h2', class_='nadpis')
        nadpis = nadpis_element.text.strip() if nadpis_element else "Neznámý nadpis"
        
        # Najdeme cenu
        cena_element = inzerat.find('div', class_='inzeratycena')
        cena = cena_element.text.strip() if cena_element else "Neznámá cena"
        
        print(f"Mobil: {nadpis}")
        print(f"Cena:  {cena}")
        print("-" * 30)

    print("Průzkum úspěšně dokončen!")

except Exception as e:
    print(f"Něco se pokazilo: {e}")