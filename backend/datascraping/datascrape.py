import pandas as pd
import requests
import time
from io import StringIO
from bs4 import BeautifulSoup

all_teams = []  # where to store all teams
years = range(2020, 2025)  # range of the dataset

# Check if the URL is accessible
if requests.get("https://www.baseball-reference.com/teams/").status_code == 429:
    print('TRY AGAIN')

# List of valid MLB team abbreviations
valid_abbrs = [
    'ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET',
    'MIA', 'HOU', 'KCR', 'LAA', 'LAD', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK',
    'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBR', 'TEX', 'TOR', 'WSN'
]

# Countdown to track progress
countdown = len(valid_abbrs)

# Date format to match the sample
date_format = '%A, %b %d'

for abbr in valid_abbrs:
    for year in years:
        year_url = f"https://www.baseball-reference.com/teams/{abbr}/{year}-schedule-scores.shtml"
        
        try:
            # Fetch the page content
            data = requests.get(year_url).text
            soup = BeautifulSoup(data, "lxml")
            stats = soup.find_all('table', class_='sortable')[0]
            
            if stats:
                try:
                    # Read the table into a DataFrame
                    team_data = pd.read_html(StringIO(str(stats)))[0]
                    team_data["Team"] = abbr  # Add team abbreviation
                    team_data["Year"] = year  # Add the year

                    # Ensure 'Date' column is correctly formatted
                    team_data["Date"] = team_data["Date"].astype(str).apply(lambda x: f"{x.strip()} {year}")
                    team_data["Date"] = pd.to_datetime(team_data["Date"], format=f"{date_format} %Y", errors='coerce')
                    team_data['Date'] = team_data['Date'].dt.strftime('%Y-%m-%d')

                    # Filter out rows where 'Unnamed: 2' column contains 'preview'
                    team_data = team_data[~team_data['Unnamed: 2'].str.contains('preview', case=False, na=False)]

                    # Append to the all_teams list
                    all_teams.append(team_data)
                    print(f"Successfully scraped {abbr} for {year}")
                    time.sleep(5)  # Avoid getting blocked
                except Exception as e:
                    print(f"Error processing data for {abbr} in {year}: {e}")
            else:
                print(f"No stats found for {abbr} in {year}")

        except requests.exceptions.RequestException as e:
            print(f"Request error for {abbr} in {year}: {e}")

    countdown -= 1
    print(f"Countdown: {countdown}")
    
    time.sleep(3)  # Avoid getting 429 too many requests error

print("Done scraping")
print(f"Number of teams collected: {len(all_teams)}")

# Combine all collected data into a single DataFrame
stat_df = pd.concat(all_teams, ignore_index=True)
stat_df.to_csv("../predict/baseball_stats.csv", index=False)
