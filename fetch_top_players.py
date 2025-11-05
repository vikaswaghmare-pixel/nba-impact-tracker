import requests
import pandas as pd
from io import StringIO

def fetch_nba_stats(season):
    # Use free CSV from Basketball-Reference (no API key needed)
    # For 2023-24: Top 20 by PER (Player Efficiency Rating)
    if season == '2023-24':
        url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    elif season == '2024-25':
        url = 'https://www.basketball-reference.com/leagues/NBA_2025_per_game.html'
    else:
        raise ValueError("Invalid season")
    
    response = requests.get(url)
    df = pd.read_html(StringIO(response.text))[0]  # Parse table
    df = df.head(20)  # Top 20
    df['Season'] = season
    return df[['Player', 'PTS', 'TRB', 'AST', 'PER']]  # Key stats: Points, Rebounds, Assists, PER

# Fetch and save
last_year = fetch_nba_stats('2023-24')
this_year = fetch_nba_stats('2024-25')
comparison = pd.concat([last_year, this_year]).pivot(index='Player', columns='Season', values=['PTS', 'TRB', 'AST'])
comparison.to_csv('top20_comparison.csv')
print(comparison.head())  # Preview