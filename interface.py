from pathlib import Path
import streamlit as st

from app import executar_analise, formatar_decimal

st.title("Analisador de Gastos")
st.write("Acompanhe suas despesas e descubra quanto você está gastando em cada categoria.")

pasta_projeto = Path(__file__).resolve().parent
caminho_arquivo = pasta_projeto / "dados" / "gastos.csv"

try:
    gastos, total, resumo = executar_analise(caminho_arquivo)
except FileNotFoundError:
    st.error("Não foi possível encontrar o arquivo de gastos.")
    st.error(f"Verifique se o arquivo existe no caminho: {caminho_arquivo}")
except ValueError as erro:
    st.error(f"Não foi possível gerar o relatório: {erro}")
else:
    st.metric("Quantidade de gastos", len(gastos))
    st.metric("Total gasto", f"R$ {formatar_decimal(total)}")

    st.subheader("Gastos por categoria")

    for item in resumo:
        categoria = item["categoria"]
        subtotal = formatar_decimal(item["subtotal"])
        percentual = formatar_decimal(item["percentual"])

        st.write(f"- {categoria}: R$ {subtotal} ({percentual}%)")