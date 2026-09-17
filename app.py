import csv
from pathlib import Path
from decimal import Decimal

def formatar_decimal(valor):
    return f"{valor:.2f}".replace(".", ",")

def carregar_gastos(caminho_arquivo):
    with open(caminho_arquivo, mode="r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        return list(leitor)

pasta_projeto = Path(__file__).resolve().parent
caminho_arquivo = pasta_projeto / "dados" / "gastos.csv"

gastos = carregar_gastos(caminho_arquivo)

total = Decimal("0.00")
totais_por_categoria = {}

for gasto in gastos:
    valor = Decimal(gasto["valor"])
    categoria = gasto["categoria"]

    total += valor

    if categoria not in totais_por_categoria:
        totais_por_categoria[categoria] = Decimal("0.00")

    totais_por_categoria[categoria] += valor

total_formatado = formatar_decimal(total)

print(f"Quantidade de gastos: {len(gastos)}")
print(f"Total de gastos: R$ {total_formatado}")

print("\nTotais por categoria:")

for categoria, subtotal in totais_por_categoria.items():
    if total != Decimal("0.00"):
        percentual = (subtotal / total) * 100
    else:
        percentual = Decimal("0.00")

    subtotal_formatado = formatar_decimal(subtotal)
    percentual_formatado = formatar_decimal(percentual)
    print(f"- {categoria}: R$ {subtotal_formatado} ({percentual_formatado}%)")