# SERC_harvest_ml.py
import os
import pandas as pd
import requests
import time
from urllib.parse import urlparse

# --- 1. CONFIGURATION ---
from dotenv import load_dotenv
load_dotenv()  # Loads variables from your local .env file

# API Keys (Set these in your .env file)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Dynamic Paths
INPUT_MAPPING = os.getenv("INPUT_PATH", "data/sample_data.csv")
OUTPUT_FILE = os.getenv("OUTPUT_PATH", "serc_multilingual_results.csv")

# --- 2. LINGUISTIC DICTIONARY ---
# This maps keywords across various languages in Spanish regions
KEYWORDS = [
    "privacidad", "cookies", "protección de datos", "tratamiento de datos", # ES
    "privadesa", "protecció de dades", "dades",                             # CAT
    "pribatutasuna", "cookieak", "datuen babesa",                           # EUS
    "privacidade",                                                          # GAL
    "legal", "aviso legal", "rgpd", "gdpr"                                  # UNIV
]

# Construct the Boolean String once
# site:domain ("kw1" OR "kw2" OR ...) before:date
kw_query_part = " OR ".join([f'"{kw}"' for kw in KEYWORDS])

def extract_domain(archive_url):
    try:
        parts = str(archive_url).split('/http')
        if len(parts) > 1:
            target_url = 'http' + parts[-1]
            netloc = urlparse(target_url).netloc
            return netloc.lower().replace('www.', '').split(':')[0].strip('/')
        return None
    except: return None

def get_multilingual_serc(domain):
    query = f'site:{domain} ({kw_query_part}) before:2018-05-25'
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {'key': GOOGLE_API_KEY, 'cx': SEARCH_ENGINE_ID, 'q': query, 'num': 1}

    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return int(data.get("searchInformation", {}).get("totalResults", "0"))
        if response.status_code in (429, 403):
            return "QUOTA_EXCEEDED"
        return 0
    except: return None

# --- 3. EXECUTION ---
# --- 3. EXECUTION ---
if __name__ == "__main__":
    df_map = pd.read_csv(INPUT_MAPPING)
    
    # NEW: Detect which ID column exists (nif or nif_anon)
    id_col = 'nif' if 'nif' in df_map.columns else 'nif_anon'
    if id_col not in df_map.columns:
        raise ValueError(f"Could not find a NIF or Anonymous ID column in {INPUT_MAPPING}")

    # Resume Logic
    done_ids = set()
    if os.path.exists(OUTPUT_FILE):
        df_done = pd.read_csv(OUTPUT_FILE)
        # Check for 'nif' in existing results; if missing, use 'nif_anon'
        existing_col = 'nif' if 'nif' in df_done.columns else 'nif_anon'
        done_ids = set(df_done[existing_col].astype(str).unique())

    print(f"🚀 Starting Harvest using column '{id_col}': {len(df_map) - len(done_ids)} firms remaining.")

    results = []
    for idx, row in df_map.iterrows():
        current_id = str(row[id_col]) # Use the dynamically detected column
        if current_id in done_ids: continue

        domain = extract_domain(row['archive_url'])
        if not domain: continue

        count = get_multilingual_serc(domain)
        if count == "QUOTA_EXCEEDED":
            print("\n🛑 QUOTA REACHED. See you in 24 hours.")
            break

        if count is not None:
            # Save using the same column name found in the input mapping
            results.append({id_col: current_id, 'domain': domain, 'serc_count': count})

        if len(results) >= 20:
            pd.DataFrame(results).to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE), index=False)
            print(f"✅ Processed {domain} | Count: {count}")
            results = []
        
        time.sleep(0.2) # Polite delay between requests

    if results:
        pd.DataFrame(results).to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE), index=False)
    print("🏁 Multilingual SERC Harvest Complete.")