import requests
import pandas as pd
from io import StringIO

def fetch_nba_stats(season):
    if season == '2023-24':
        url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    elif season == '2024-25':
        url = 'https://www.basketball-reference.com/leagues/NBA_2025_per_game.html'
    else:
        raise ValueError("Invalid season")
    
    response = requests.get(url)
    df = pd.read_html(StringIO(response.text))[0].head(20)
    df['Season'] = season
    
    # Fetch advanced for impact (WS/48: Win Shares per 48 min — measures team wins contributed)
    adv_url = url.replace('per_game', 'advanced')
    adv_df = pd.read_html(StringIO(requests.get(adv_url).text))[0].head(20)
    df['WS/48'] = adv_df['WS/48']  # Team impact proxy
    return df[['Player', 'PTS', 'TRB', 'AST', 'WS/48']]

# Fetch, compare, save
last_year = fetch_nba_stats('2023-24')
this_year = fetch_nba_stats('2024-25')
comparison = pd.concat([last_year, this_year]).pivot(index='Player', columns='Season', values=['PTS', 'TRB', 'AST', 'WS/48'])
comparison.to_csv('top20_comparison.csv')
print("Top 20 Comparison with Impact (WS/48):")
print(comparison)# Updated: Added WS/48 impact metric
 