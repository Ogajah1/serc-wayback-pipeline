import pandas as pd
import uuid

# 1. Load your private research data
df = pd.read_csv("C:/PatentData/nif_url_map.csv")

# 2. Create a unique, random ID for each firm to pseudonymize NIFs. Ensures we can link results back to real NIFs if needed
nif_map = {nif: f"FIRM_{i:04d}" for i, nif in enumerate(df['nif'].unique())}

# 3. Apply the mapping
df['nif_anon'] = df['nif'].map(nif_map)

# 4. Save the "Public" version for the 'data' folder: retains only anonumous IDs and archive URLs
df_public = df[['nif_anon', 'archive_url']].head(50) # Take a small sample
df_public.to_csv("data/sample_data.csv", index=False)

# 5. Saving the "Private Key" (NIF <-> Anonymous ID mapping)
pd.DataFrame(list(nif_map.items()), columns=['nif', 'nif_anon']).to_csv("C:/PatentData/private_key.csv", index=False)

print("✅ Public sample created in data/sample_data.csv")