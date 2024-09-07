from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

all_teams = [] # where to store all teams

if requests.get("https://www.baseball-reference.com/teams/").status_code == 429:
    print('try again')

html = requests.get("https://www.baseball-reference.com/teams/").text



soup = BeautifulSoup(html, "html.parser")

table = soup.find_all('table', class_ ='stats_table')[0] # first table

links = table.find_all('a') # all links in table
links = [l.get("href") for l in links if l.get("href") and '/teams/' in l.get("href")]

team_urls = [f"https://www.baseball-reference.com/teams/{l}" for l in links] # formatting links

for url in team_urls:
    team_name = url.split('/')[-1]
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    stats = soup.find_all('table', class_ = 'stats_table')[0]

    # dataframe
    team_data = pd.read_html(str(stats))[0]
    team_data["Team"] = team_name
    all_teams.append(team_data)
    
    time.sleep(10)

print(f"Number of teams collected: {len(all_teams)}")

stat_df = pd.concat(all_teams)

stat_df.to_csv("baseball_stats.csv")