import csv
from pathlib import Path
#from decimal import Decimal

pasta_projeto = Path(__file__).resolve().parent
caminho_arquivo = pasta_projeto / "dados" / "gastos.csv"

with open(caminho_arquivo, mode = "r", encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter = ";")
    gastos = list(leitor)

for gasto in gastos:
    print(gasto)