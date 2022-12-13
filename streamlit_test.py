import pandas as pd
import streamlit as st
import csv



# Title of the app
st.title('Saldo de Gols por Ano e País na Copa do Mundo')

# Read the data
df_goals = pd.read_csv('data/goalscorers.csv', parse_dates=['date'])
df_results = pd.read_csv('data/results.csv', parse_dates=['date'])
df_shootouts = pd.read_csv('data/shootouts.csv', parse_dates=['date'])
conf_names = pd.read_csv('data\confederation_names.csv',encoding='ISO-8859-1', sep = ';', engine='python')


# Filter the data to check all the tournaments and countries in the dataset
df_results.tournament.unique()
countries = df_results.country.unique()

# Set the base URL for the API
api_url = 'https://countryflagsapi.com/png'

# Open the CSV file for writing
with open('flags.csv', 'w') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['country', 'flag_URL'])

    # Loop through the countries
    for country in countries:
        # Build the URL for the flag image
        flag_url = f'{api_url}/{country}'

        # Write the country name and flag URL to the CSV file
        writer.writerow([country, flag_url])

# Read the CSV file with the flags
flags = pd.read_csv('data/flags.csv', encoding='ISO-8859-1', engine='python')


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

# Export the data to a CSV file
to_flourish.to_csv('data/to_flourish.csv', index=False)

# plot data
st.components.v1.iframe(src="https://public.flourish.studio/visualisation/12149711/", width=800, height=700)
