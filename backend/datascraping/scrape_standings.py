import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

# Fetch the MLB standings data from the website
response = requests.get("https://www.mlb.com/standings/")
if response.status_code == 429:
    print('TRY AGAIN')
    exit()

# Parse the website content using BeautifulSoup
data = response.text
soup = BeautifulSoup(data, 'lxml')
stats = soup.find('div', class_="tablestyle__TableContainer-sc-wsl6eq-2 gzGGfc")

# Convert the table data into a pandas DataFrame
team_data = pd.read_html(StringIO(str(stats)))[0]

# Dictionary mapping full team names to their abbreviations
team_abbrs = {
    'New York Yankees': 'NYY', 'Baltimore Orioles': 'BAL', 'Boston Red Sox': 'BOS', 'Tampa Bay Rays': 'TBR', 'Toronto Blue Jays': 'TOR',
    'Cleveland Guardians': 'CLE', 'Detroit Tigers': 'DET', 'Kansas City Royals': 'KCR', 'Minnesota Twins': 'MIN', 'Chicago White Sox': 'CHW',
    'Houston Astros': 'HOU', 'Seattle Mariners': 'SEA', 'Texas Rangers': 'TEX', 'Oakland Athletics': 'OAK', 'Los Angeles Angels': 'LAA',
    'Philadelphia Phillies': 'PHI', 'New York Mets': 'NYM', 'Atlanta Braves': 'ATL', 'Washington Nationals': 'WSN', 'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL', 'Chicago Cubs': 'CHC', 'St. Louis Cardinals': 'STL', 'Cincinnati Reds': 'CIN', 'Pittsburgh Pirates': 'PIT',
    'Arizona Diamondbacks': 'ARI', 'Los Angeles Dodgers': 'LAD', 'San Diego Padres': 'SDP', 'San Francisco Giants': 'SFG', 'Colorado Rockies': 'COL'
}

# List of division headers to identify divisions
division_headers = ['AL East', 'AL Central', 'AL West', 'NL East', 'NL Central', 'NL West']

# Initialize the 'Rank' column with None values
team_data['Rank'] = None

# Variable to store the current rank
current_rank = 1

# Iterate through each row to assign ranks and update team names with abbreviations
for index, row in team_data.iterrows():
    if row.iloc[0] in division_headers:
        # Reset rank to 1 when encountering a new division
        current_rank = 1
    else:
        # Clean up the full team name by stripping whitespace
        full_name = row.iloc[0].strip()

        # Check if the full name ends with 'x' or 'y' and remove only if it's a playoff indicator
        if full_name.endswith(('x', 'y')):
            # Check if it's not one of the team names before modifying
            potential_name = full_name[:-1]
            if potential_name in team_abbrs or potential_name in team_abbrs.values():
                full_name = potential_name  # Only strip if it matches a known team

        # Assign the current rank and increment for the next team
        team_data.at[index, 'Rank'] = current_rank
        current_rank += 1

        # Replace full team name with abbreviation if it exists in the mapping
        if full_name in team_abbrs:
            team_data.at[index, "abbr"] = team_abbrs[full_name]
        else:
            print(f"Warning: '{full_name}' not found in abbreviation mapping.")  # Debugging output for unmatched names

# Display the updated DataFrame
print(team_data)

# Optionally save to CSV
team_data.to_csv("../app/current_stats.csv", index=False)
