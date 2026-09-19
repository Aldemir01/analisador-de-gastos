import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation

def formatar_decimal(valor):
    return f"{valor:.2f}".replace(".", ",")

def carregar_gastos(caminho_arquivo):
    with open(caminho_arquivo, mode="r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        colunas_obrigatorias = {"data", "descricao","categoria", "valor"}
        
        colunas_encontradas = set(leitor.fieldnames or [])

        colunas_faltantes = colunas_obrigatorias - colunas_encontradas

        if colunas_faltantes:
            nomes = ", ".join(sorted(colunas_faltantes))
            raise ValueError(f"Colunas obrigatórias ausentes: {nomes}")

        gastos = []

        for numero_linha, gasto in enumerate(leitor, start=2):
            for coluna in sorted(colunas_obrigatorias):
                conteudo = gasto[coluna]

                if conteudo is None or conteudo.strip() == "":
                    raise ValueError(f"Linha {numero_linha}: o campo '{coluna}' está vazio.")

                gasto[coluna] = conteudo.strip()

            gastos.append(gasto)

        return gastos

def calcular_totais(gastos):
    total = Decimal("0.00")
    totais_por_categoria = {}

    for numero_linha, gasto in enumerate(gastos, start=2):
        try:
            valor = Decimal(gasto["valor"])
        except InvalidOperation:
            raise ValueError(f"Linha {numero_linha}: valor inválido '{gasto['valor']}' . Use um número como 150.50.") from None
        
        if not valor.is_finite():
            raise ValueError(f"Linha {numero_linha}: o valor deve ser um número finito.")

        categoria = gasto["categoria"]
        total += valor

        if categoria not in totais_por_categoria:
            totais_por_categoria[categoria] = Decimal("0.00")

        totais_por_categoria[categoria] += valor

    return total, totais_por_categoria

def exibir_relatorio(gastos, total, totais_por_categoria):
    total_formatado = formatar_decimal(total)

    print(f"Quantidade de gastos: {len(gastos)}")
    print(f"Total gasto: R$ {total_formatado}")

    print("\nGastos por categoria:")

    for categoria, subtotal in totais_por_categoria.items():
        if total != Decimal("0.00"):
            percentual = (subtotal / total) * 100
        else:
            percentual = Decimal("0.00")

        subtotal_formatado = formatar_decimal(subtotal)
        percentual_formatado = formatar_decimal(percentual)

        print(
            f"\n- {categoria}: R$ {subtotal_formatado}" 
            f"({percentual_formatado}%)"
        )

def main():
    pasta_projeto = Path(__file__).resolve().parent
    caminho_arquivo = pasta_projeto / "dados" / "gastos.csv"

    try:
        gastos = carregar_gastos(caminho_arquivo)
        total, totais_por_categoria = calcular_totais(gastos)
    except FileNotFoundError:
        print("Não foi possível encontrar o arquivo de gastos.")
        print(f"Verifique se o arquivo existe no caminho: {caminho_arquivo}")
    except ValueError as erro:
        print(f"Não foi possível gerar o relatório: {erro}")
    else:
        exibir_relatorio(gastos, total, totais_por_categoria)

if __name__ == "__main__":
    main()