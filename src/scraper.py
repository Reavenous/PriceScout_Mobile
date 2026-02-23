import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

print("--- PriceScout Mobile: Velký sběr dat (Mise 3000) ---")

# Vytvoříme složku pro uložení dat
os.makedirs(os.path.join("data", "raw"), exist_ok=True)
cesta_k_souboru = os.path.join("data", "raw", "mobily_raw.csv")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

vsechna_data = []

# Pro 3000 inzerátů (20 na stránku) potřebujeme 150 stránek
POCET_STRANEK = 150

for stranka in range(POCET_STRANEK):
    offset = stranka * 20
    
    # OPRAVA BAZOŠ LOGIKY: První stránka nesmí mít /0/
    if offset == 0:
        url = "https://mobil.bazos.cz/"
    else:
        url = f"https://mobil.bazos.cz/{offset}/"
    
    print(f"Stahuji stránku {stranka + 1}/{POCET_STRANEK} (Odkaz: {url})")
    
    try:
        odpoved = requests.get(url, headers=headers)
        odpoved.raise_for_status()
        soup = BeautifulSoup(odpoved.text, 'lxml')
        
        inzeraty = soup.find_all('div', class_='inzeraty')
        
        # Pojistka: Pokud už na stránce nejsou inzeráty, ukončíme to
        if not inzeraty:
            print("Na této stránce už nejsou žádné inzeráty. Končím stahování.")
            break
        
        for inzerat in inzeraty:
            nadpis_el = inzerat.find('h2', class_='nadpis')
            nadpis = nadpis_el.text.strip() if nadpis_el else ""
            
            cena_el = inzerat.find('div', class_='inzeratycena')
            cena = cena_el.text.strip() if cena_el else ""
            
            popis_el = inzerat.find('div', class_='popis')
            popis = popis_el.text.strip() if popis_el else ""
            
            vsechna_data.append({
                "Nadpis": nadpis,
                "Cena": cena,
                "Popis": popis
            })
            
        # DŮLEŽITÉ: Pauza 1.5 až 3 vteřiny, abychom nedostali ban!
        time.sleep(random.uniform(1.5, 3.0))
        
    except Exception as e:
        print(f"Chyba na stránce {stranka + 1}: {e}")
        print("Zastavuji stahování, ale uložím to, co už máme.")
        break # Uložíme aspoň to, co se stihlo stáhnout před chybou

# Uložení do tabulky
print("\nUkládám data do CSV tabulky...")
df = pd.DataFrame(vsechna_data)
df.to_csv(cesta_k_souboru, index=False, encoding='utf-8')

print(f"HOTOVO! Staženo {len(df)} inzerátů a uloženo do {cesta_k_souboru}.")