import re
import pandas as pd

def TravelexExtratoCC(csv_path, texto):
    # Padrão regex
    padrao = r"\d{2}/\d{2}/\d{4}\n(\d{2}/\d{2}/\d{4})\n\d{2}:\d{2}\n([\w\sç]*\n(?!.*LIQUIDACAO)\w*)\n([\w\s\d\n./:|-]*(?=))\b(?:Sim|Não)\b ([-.\d,\d{2}]*(?=)) ([-.\d,\d{2}]*(?=))"
    padrao_saldo_inicial = r"(.+) (Saldo Inicial) (.+)"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    match_saldo_inicial = re.findall(padrao_saldo_inicial, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Tipo', 'Detalhes', 'Valor', 'Saldo']

     # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in match_saldo_inicial:
            matches_saldo_inicial_ordenado = [match[0], match[1], '', '', match[2]]
            matches_ordenados.append(matches_saldo_inicial_ordenado)
        for match in matches:
            matches_ordenado = [match[0], match[1], match[2], match[3], match[4]]
            matches_ordenados.append(matches_ordenado)

        df = pd.DataFrame(matches_ordenados, columns=colunas)
        
        def itera_valor(coluna):
            for index, row in df.iterrows():
                # Remover pontos e vírgulas
                cleaned_value = str(row[coluna]).replace('.', '').replace(',', '')

                try:
                    # Tentar converter para float
                    float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                    # Atualizar o valor na coluna 'Valor'
                    df.at[index, coluna] = float_value
                # Tratar casos onde a conversão falha
                except ValueError:
                    # Atribuir um valor padrão ou NaN para valores inválidos
                    df.at[index, coluna] = ''

            # Converter a coluna "Valor" para tipo numérico
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        
        itera_valor('Valor')
        itera_valor('Saldo')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df