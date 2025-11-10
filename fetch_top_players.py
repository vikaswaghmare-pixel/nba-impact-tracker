from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import teams
import pandas as pd
import time

def fetch_nba_stats(season):
    """
    Fetch NBA stats for a given season using the official NBA API
    
    Args:
        season: Season in format '2023-24'
    
    Returns:
        DataFrame with top 20 players by points
    """
    try:
        print(f"Fetching data for {season}...")
        
        # The NBA API uses different season format - needs to be like '2023-24'
        # leagueleaders endpoint gets player stats
        leaders = leagueleaders.LeagueLeaders(
            season=season,
            league_id='00',  # NBA
            per_mode48='PerGame',  # Per game stats
            scope='S',  # Season scope
            season_type_all_star='Regular Season',
            stat_category_abbreviation='PTS'  # Sort by points
        )
        
        # Get the data as a dataframe
        df = leaders.get_data_frames()[0]
        
        # Select top 20 players
        df_top20 = df.head(20)
        
        # Select and rename relevant columns for readability
        df_result = df_top20[[
            'PLAYER', 'TEAM_ABBREVIATION', 'GP', 'MIN',
            'PTS', 'REB', 'AST', 'FG_PCT', 'FG3_PCT', 'FT_PCT'
        ]].copy()
        
        # Rename columns
        df_result.columns = ['Player', 'Team', 'GP', 'MIN', 'PTS', 'REB', 'AST', 'FG%', '3P%', 'FT%']
        
        print(f"Successfully fetched {len(df_result)} players for {season}")
        return df_result
        
    except Exception as e:
        print(f"Error fetching data for {season}: {e}")
        print("Make sure you have installed nba_api: pip install nba_api")
        return None

# Main execution
if __name__ == "__main__":
    # Fetch data for multiple seasons
    last_year = fetch_nba_stats('2023-24')
    
    # Add delay to be respectful to the API
    time.sleep(1)
    
    this_year = fetch_nba_stats('2024-25')
    
    # Display results if successful
    if last_year is not None:
        print("\n" + "="*80)
        print("Top 20 Players 2023-24 Season (by PPG)")
        print("="*80)
        print(last_year.to_string(index=False))
    
    if this_year is not None:
        print("\n" + "="*80)
        print("Top 20 Players 2024-25 Season (by PPG)")
        print("="*80)
        print(this_year.to_string(index=False))
    
    # Save to CSV if needed
    if last_year is not None:
        last_year.to_csv('nba_stats_2023-24.csv', index=False)
        print("\n✓ Saved 2023-24 stats to nba_stats_2023-24.csv")
    
    if this_year is not None:
        this_year.to_csv('nba_stats_2024-25.csv', index=False)
        print("✓ Saved 2024-25 stats to nba_stats_2024-25.csv")