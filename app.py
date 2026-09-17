import csv
from pathlib import Path
from decimal import Decimal

pasta_projeto = Path(__file__).resolve().parent
caminho_arquivo = pasta_projeto / "dados" / "gastos.csv"

with open(caminho_arquivo, mode = "r", encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter = ";")
    gastos = list(leitor)

total = Decimal("0.00")


for gasto in gastos:
    valor = Decimal(gasto["valor"])
    total += valor

total_formatado = f"{total:.2f}".replace(".", ",")

print(f"Quantidade de gastos: {len(gastos)}")
print(f"Total de gastos: R$ {total_formatado}")