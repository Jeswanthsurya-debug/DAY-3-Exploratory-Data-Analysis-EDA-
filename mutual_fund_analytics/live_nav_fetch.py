import requests
import pandas as pd

# The 6 specific fund codes required by your assignment dashboard
schemes = {
    "125497": "HDFC Top 100 Direct",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "110902": "Axis Bluechip",
    "120841": "Kotak Bluechip"
}

all_records = []

print("--- Starting Live API Data Extraction ---")

for code, name in schemes.items():
    print(f"📡 Connecting to API for: {name} (Code: {code})...")
    url = f"https://api.mfapi.in/mf/{code}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        nav_entries = json_data.get('data', [])
        
        # Loop through daily pricing data and save it
        for entry in nav_entries:
            all_records.append({
                "scheme_code": code,
                "scheme_name": name,
                "date": entry.get("date"),
                "nav": entry.get("nav")
            })
    else:
        print(f"❌ Failed to get data for code {code}")

# Convert all collected data into a spreadsheet table
live_dataframe = pd.DataFrame(all_records)

# Save it to a brand new CSV file inside your folder
output_filename = "live_nav_history.csv"
live_dataframe.to_csv(output_filename, index=False)

print("\n=========================================")
print(f"✅ SUCCESS: Saved API data to {output_filename}")
print(f"📊 Total Records Fetched: {len(live_dataframe)}")
print("=========================================")