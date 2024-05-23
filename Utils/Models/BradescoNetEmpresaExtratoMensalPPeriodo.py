import re
import pandas as pd

def BradescoNetEmpresaExtratoMensalPPeriodo(csv_path, texto):
    # Padrão regex
    padrao = r"^(\d{2}/\d{2}/\d{4})*\s*([\w\d./:& -]*\s*[\w\d./:& -]*)\s*(\d+)*\s+([-.\d,]+,\d{2}\b-*)\s*([-.\d,]+,\d{2}\b-*)*"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Lançamento', 'Documento', 'Valor', 'Saldo']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

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