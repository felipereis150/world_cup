import pandas as pd
import streamlit as st

# Title of the app
st.title('Saldo de Gols por Ano e País na Copa do Mundo')

# Read the data
df_results = pd.read_csv('https://github.com/felipereis150/world_cup/blob/main/data/results.csv?raw=true', parse_dates=['date'])
conf_names = pd.read_csv('https://github.com/felipereis150/world_cup/blob/main/data/confederation_names.csv?raw=true',encoding='ISO-8859-1', sep = ';', engine='python')


# Filter the data to check all the tournaments and countries in the dataset
df_results.tournament.unique()
countries = df_results.country.unique()

# Set the base URL for the API
api_url = 'https://countryflagsapi.com/png'

flags = []
# Loop through the countries
for country in countries:

    # Build the URL for the flag image
    flag_url = f'{country},{api_url}'
    flags.append([country, flag_url])

flags = pd.DataFrame(flags, columns=['country', 'flag_URL'])


# Filter the data to check all the countries in the dataset
worldCup = df_results[df_results['tournament'] == 'FIFA World Cup']

# Add year column
worldCup['year'] = worldCup['date'].dt.year

# Reshape data to have 1 row per match and 2 columns per team (home and away) keeping the year, the date, the tournament, the city, the country, the neutral field and the score
worldCup = worldCup.melt(id_vars=['year', 'date', 'home_team', 'away_team', 'tournament', 'city', 'country', 'neutral'], value_vars=['home_score', 'away_score'], var_name='score_type', value_name='score')
worldCup = worldCup.melt(id_vars=['year', 'date', 'tournament', 'city', 'country', 'neutral', 'score_type', 'score'], value_vars=['home_team', 'away_team'], var_name='team_type', value_name='team')

# Filter the data to keep only the home team and the score
total_score_by_team = worldCup.groupby(['year', 'team'])['score'].sum().reset_index().sort_values(by='year', ascending=True)

# Calculate the cumulative score by team
total_score_by_team['cum_score'] = total_score_by_team.groupby('team')['score'].cumsum()

# Merge the flags with the confederation names
flags = flags.merge(conf_names, left_on='country', right_on='country', how='left')

# Merge the flags with the total score by team
total_score_by_team = total_score_by_team.merge(flags, left_on='team', right_on='country', how='left')

# Drop the columns that are not needed
to_flourish = total_score_by_team.drop(['country', 'score'], axis=1)

# reshape data to flourish format having 1 row per team and 1 column per year keeping the cumulative score, the flag and the acronysm as columns
to_flourish = to_flourish.pivot_table(index=['team', 'flag_URL', 'acronysm'], columns='year', values='cum_score', aggfunc='first').reset_index().fillna(0)