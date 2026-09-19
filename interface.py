from pathlib import Path
import streamlit as st

from app import carregar_gastos, calcular_totais, formatar_decimal, exibir_relatorio

st.title("Analisador de Gastos")
st.write("Acompanhe suas despesas e descubra quanto você está gastando em cada categoria.")