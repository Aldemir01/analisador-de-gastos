from pathlib import Path
import streamlit as st
import plotly.express as px

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
    
    coluna_quantidade, coluna_total = st.columns(2)

    with coluna_quantidade:
        st.metric("Quantidade de gastos", len(gastos))
    with coluna_total:
        st.metric("Total gasto", f"R$ {formatar_decimal(total)}")

    st.subheader("Gastos por categoria")

    dados_tabela = []
    dados_grafico = []
    dados_pizza = []

    for item in resumo:
        dados_tabela.append({
            "Categoria": item["categoria"],
            "Subtotal": f"R$ {formatar_decimal(item['subtotal'])}",
            "Percentual": f"{formatar_decimal(item['percentual'])}%",
        })
        dados_grafico.append({
            "categoria": item["categoria"],
            "subtotal": float(item["subtotal"])
        })
        dados_pizza.append({
            "categoria": item["categoria"],
            "percentual": float(item["percentual"])
        })
    st.table(dados_tabela)

    st.subheader("Percentual dos Gastos")

    figura_pizza = px.pie(dados_pizza, names="categoria", values="percentual", title="Percentual dos Gastos por Categoria")
    st.plotly_chart(figura_pizza, width='stretch')

    st.subheader("Distribuição de Gastos")

    st.bar_chart(data=dados_grafico, x="categoria", y="subtotal")