import streamlit as st
import pandas as pd
st.markdown("""

# Saldo de Gols por Ano e País na Copa do Mundo
O código dessa visualização está hospedado no [GitHub](https://github.com/felipereis150/world_cup).

Abaixo temos uma visualização interativa da soma cumulativa de gols por time e confederação em Copas do Mundo,  de 1930 a 2022. O gráfico foi feito utilizando [Flourish](https://flourish.studio/) e os dados são do [Kagle](The%20data%20is%20gathered%20from%20several%20sources%20including%20but%20not%20limited%20to%20Wikipedia,%20rsssf.com,%20and%20individual%20football%20associations%27%20websites.), é possível pausar  ou avançar a animação no controle abaixo das barras e. As imagens das bandeiras foram obtidas através [dessa](https://countryflagsapi.com/) API. Por fim, esse dashboard foi construído usando o [Streamlit](https://streamlit.io/).

"""
)

# add slider to year
year = st.slider('Ano', 1930, 2022, 1930)

# plot data
goal_difference_in_world_cup = st.components.v1.iframe(src="https://public.flourish.studio/visualisation/12149711/", width=800, height=700)

st.markdown(""" como podemos observar, somente em 1976 a Alemanha ultrapassa o Brasil em saldo de gols matém essa vantagem até os dias de hoje. """)


''' 
Não tenho certeza de como quero continuar. Não parece ser possível trazer os dataframes do arquivo EDA para esse arquivo. No entando, não vale a pena fazer a análise toda de novo aqui só pra ter ela no streamlit. 

Uma abordagem possível seria transformar o arquivo EDA em um módulo e importar ele aqui. Mas isso não parece ser uma boa prática, já que perco o controle do que está sendo executado e os gráficos que fiz lá. Outro trade-off é que perco a chance de mostrar o código que fiz para fazer a análise passo a passo. Fazer a análise aqui mesmo suja muito o código da visualização do dashboard. 

Uma outra possibilidade é fazer uma função que retorna os dataframes que eu quero e importar ela aqui. Mas isso não parece ser uma boa prática também, já que perco a chance de mostrar o código que fiz para fazer a análise passo a passo.

Posso juntar os dois arquivos (analisys e EDA) em um só, mas isso não parece ser uma boa prática também, já que perco a chance de mostrar o código que fiz para fazer a análise passo a passo.

quero plotar os seguintes gráficos no dashboard


acho que seria tudo ao longo dos anos


cidades que houveram jogos [mapa]
quem fez mais gols [line]
países que mais houveram gols [barra]
cidades que houveram mais hols [tabela]


'''