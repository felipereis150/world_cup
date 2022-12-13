import streamlit as st

st.markdown("""

# Saldo de Gols por Ano e País na Copa do Mundo
O código dessa visualização está hospedado no [GitHub](https://github.com/felipereis150/world_cup).

Abaixo temos uma visualização interativa da soma cumulativa de gols por time e confederação em Copas do Mundo,  de 1930 a 2022. O gráfico foi feito utilizando [Flourish](https://flourish.studio/) e os dados são do [Kagle](The%20data%20is%20gathered%20from%20several%20sources%20including%20but%20not%20limited%20to%20Wikipedia,%20rsssf.com,%20and%20individual%20football%20associations%27%20websites.), é possível pausar  ou avançar a animação no controle abaixo das barras e. As imagens das bandeiras foram obtidas através [dessa](https://countryflagsapi.com/) API. Por fim, esse dashboard foi construído usando o [Streamlit](https://streamlit.io/).

"""
)
# plot data
st.components.v1.iframe(src="https://public.flourish.studio/visualisation/12149711/", width=800, height=700)

st.markdown(""" como podemos observar, somente em 1976 a Alemanha ultrapassa o Brasil em saldo de gols matém essa vantagem até os dias de hoje. """)