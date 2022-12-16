import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(layout="wide")
# importing the data

results  = pd.read_csv("https://github.com/felipereis150/world_cup/blob/main/data/results.csv?raw=true", parse_dates=['date'])
goalscoers  = pd.read_csv("https://github.com/felipereis150/world_cup/blob/main/data/goalscorers.csv?raw=true", parse_dates=['date'])
shootouts  = pd.read_csv("https://github.com/felipereis150/world_cup/blob/main/data/shootouts.csv?raw=true", parse_dates=['date'])
conf_names = pd.read_csv('https://github.com/felipereis150/world_cup/blob/main/data/confederation_names.csv?raw=true',encoding='ISO-8859-1', sep = ';', engine='python')
cities = pd.read_csv('https://github.com/felipereis150/world_cup/blob/EDA/data/worldcities.csv?raw=true')

# creating a new dataframe with all the data

futebol_df = results.merge(shootouts, on=['home_team', 'away_team'], how='left')
futebol_df = futebol_df.merge(goalscoers, on=['home_team', 'away_team'], how='left')
futebol_df = futebol_df.merge(conf_names, left_on='country', right_on='country', how='left')

# cleaning and transforming the data

world_cup = futebol_df[futebol_df['tournament'] == 'FIFA World Cup']
world_cup['year'] = world_cup['date'].dt.year
world_cup['decade'] = world_cup['year'].apply(lambda x: str(x)[2:3] + '0s')
world_cup = world_cup[world_cup['year'] > 1930]
world_cup.reset_index(inplace=True)
world_cup['year'] = world_cup['year'].astype(int)
cities.drop_duplicates(subset=['city_ascii'], inplace=True)

# merging the data

world_cup = world_cup.merge(cities[['city', 'lat', 'lng']], left_on='city', right_on='city', how='left')
world_cup = world_cup.drop(columns=['index', 'date_x', 'neutral', 'date_y', 'own_goal', 'minute', 'penalty'])
world_cup.rename(columns={'acronysm': 'conf', 'lng': 'lon'}, inplace=True)

# creating a new column with the winner of the match
world_cup['winner'] = np.where(world_cup['home_score'] > world_cup['away_score'], world_cup['home_team'], world_cup['away_team'])

# Top 10 teams with most wins

df_matches = world_cup[['home_team', 'away_team', 'home_score', 'away_score', 'winner']].drop_duplicates()
wins = df_matches.groupby('winner').size().sort_values(ascending=False)
top_10_teams = wins.head(10)

# best scorers
best_scorer = world_cup['scorer'].value_counts().head(10)

# cities there was most world cup matches with lat and lon
city_matches = world_cup[['home_team', 'away_team', 'city', 'lat', 'lon']].groupby(['home_team', 'away_team', 'city']).count().reset_index()
city_counts = city_matches['city'].value_counts()
top_cities = city_counts.head(100)
df_top_cities = world_cup[['city', 'lat', 'lon']][world_cup['city'].isin(top_cities.index)].drop_duplicates()
df_top_cities['num_games'] = top_cities.values
df_top_cities.sort_values(by='num_games', ascending=False, inplace=True)
df_top_cities.dropna(inplace=True)


st.markdown("""

O código dessa visualização está hospedado no [GitHub](https://github.com/felipereis150/world_cup).

Abaixo temos uma visualização interativa da soma cumulativa de gols por time e confederação em Copas do Mundo,  de 1930 a 2022. O gráfico foi feito utilizando [Flourish](https://flourish.studio/) e os dados são do [Kagle](The%20data%20is%20gathered%20from%20several%20sources%20including%20but%20not%20limited%20to%20Wikipedia,%20rsssf.com,%20and%20individual%20football%20associations%27%20websites.).
É possível pausar  ou avançar a animação no controle abaixo das barras e. As imagens das bandeiras foram obtidas através [dessa](https://countryflagsapi.com/) API. Por fim, esse dashboard foi construído usando o [Streamlit](https://streamlit.io/).

"""
)

st.markdown(' ### Saldo de gols por ano e país na Copa do Mundo')

st.markdown(""" *Como podemos observar, somente em 1976 a Alemanha ultrapassa o Brasil em saldo de gols matém essa vantagem até os dias de hoje.* """)
# plot data
goal_difference_in_world_cup = st.components.v1.iframe(src="https://public.flourish.studio/visualisation/12149711/", width=1280, height=750)

bar_chart_teams = top_10_teams
bar_chart_scorer = best_scorer

st.markdown(' ### Times que mais venceram jogos da Copa do Mundo')
st.markdown(""" *O Brazil supera a Alemanha em número de jogos por 8 jogos (10,66%)* """)

st.bar_chart(bar_chart_teams)
st.markdown(' ### Melhores artilheiros da Copa do Mundo')
st.bar_chart(bar_chart_scorer)

st.markdown(' ### Cidades que mais sediaram jogos da Copa do Mundo')
col1, col2 = st.columns([3, 1])

col1.map(df_top_cities)
col2.dataframe(df_top_cities[['city', 'num_games']])
