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
        
        # Print available columns for debugging
        print(f"Available columns: {df.columns.tolist()}")
        
        # Select top 20 players
        df_top20 = df.head(20)
        
        # Map common column names (API might use different names)
        column_mapping = {
            'PLAYER': 'Player',
            'TEAM': 'Team',
            'TEAM_ABBREVIATION': 'Team',
            'TEAM_ID': 'Team',
            'GP': 'GP',
            'MIN': 'MIN',
            'PTS': 'PTS',
            'REB': 'REB',
            'AST': 'AST',
            'FG_PCT': 'FG%',
            'FG3_PCT': '3P%',
            'FT_PCT': 'FT%'
        }
        
        # Find which columns actually exist
        cols_to_select = []
        for col in df_top20.columns:
            if col in column_mapping:
                cols_to_select.append(col)
        
        # Select available columns
        df_result = df_top20[cols_to_select].copy()
        
        # Rename columns to friendly names
        rename_dict = {col: column_mapping[col] for col in cols_to_select}
        df_result.rename(columns=rename_dict, inplace=True)
        
        print(f"Successfully fetched {len(df_result)} players for {season}")
        return df_result
        
    except Exception as e:
        print(f"Error fetching data for {season}: {e}")
        import traceback
        traceback.print_exc()
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

