import pandas as pd
from pynput import keyboard
import time
import os

# --- KONFIGURACE ---
# Cesta k souboru: Jde o složku výš (..) a pak do data/raw
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
DATA_FILE = os.path.join(project_root, "data", "raw", "keystrokes_raw.csv")

# Změň si na to, co chceš trénovat! (Ideálně 10-15 znaků)
HESLO_PRO_SBER = "tajneheslo123" 

# Zajistíme, že složka existuje
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

print(f"--- TYPE SENTINEL: SBĚR DAT ---")
print(f"Cílové heslo pro opisování: '{HESLO_PRO_SBER}'")
print(f"Data se budou ukládat do: {DATA_FILE}")
jmeno = input("Zadej jméno uživatele (např. 'HrotBagr' nebo 'Vetrelec1'): ")

# Seznam pro ukládání dat v paměti
temp_data = []

print("\nPOKYNY:")
print("1. Napiš heslo a stiskni ENTER.") # <--- TADY BYLA CHYBA (už je opraveno)
print("2. Pokud se spleteš, stiskni BACKSPACE (celý pokus se zahodí).")
print("3. Pro ukončení stiskni ESC.")
print("---------------------------------------------------")
print("Můžeš začít psát...")

def on_press(key):
    try:
        # Zkusíme získat znak (písmeno/číslo)
        key_char = key.char
    except AttributeError:
        # Speciální klávesy (Enter, Space, atd.)
        key_char = str(key).replace("Key.", "")

    # Uložíme čas stisku
    temp_data.append({
        'user': jmeno,
        'key': key_char,
        'action': 'press',
        'timestamp': time.time()
    })

def on_release(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key).replace("Key.", "")

    # Uložíme čas uvolnění
    temp_data.append({
        'user': jmeno,
        'key': key_char,
        'action': 'release',
        'timestamp': time.time()
    })

    # Logika pro ovládání (Enter = Uložit, Backspace = Smazat pokus, Esc = Konec)
    if key == keyboard.Key.enter:
        save_to_csv()
        print(f" -> Pokus uložen! Zadej heslo znovu: '{HESLO_PRO_SBER}'")
        temp_data.clear() # Vyčistit paměť pro další pokus
        
    elif key == keyboard.Key.backspace:
        print(" -> CHYBA! Pokus zahozen. Zkus to znovu.")
        temp_data.clear()

    elif key == keyboard.Key.esc:
        print("\nUkončování sběru dat...")
        return False # Zastaví listener

def save_to_csv():
    # Pokud soubor neexistuje, vytvoříme ho s hlavičkou
    file_exists = os.path.isfile(DATA_FILE)
    
    df = pd.DataFrame(temp_data)
    # Uložíme jen pokud máme data (ošetření prázdného Enteru)
    if not df.empty:
        df.to_csv(DATA_FILE, mode='a', header=not file_exists, index=False)

# Spuštění naslouchání klávesnici
# Tady pozor na odsazení - musí to být takto zarovnané doleva
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()