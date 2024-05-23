import re
import pandas as pd

def BancoDoBrasilEmpresaExtratoCC(csv_path, texto):
    # Padrão regex
    padrao = r"([\d/+]+\d{4})+ (\d{4}) (\d{5}) (.+) +([ \d,.-]+,\d{2})\s*(\w)\s*"
    
    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Agência Origem', 'lote', 'Histórico', 'Valor RS', 'Operador']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            valor = row['Valor RS']
            operador = row['Operador']

            # Remover pontos e vírgulas do valor
            cleaned_value = str(valor).replace('.', '').replace(',', '')

            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if row['Operador'] == "D":
                cleaned_value = '-' + cleaned_value[0:]   

            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                # Atualizar o valor na coluna 'Valor'
                df.at[index, 'Valor RS'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor RS'] = ''

        # Converter a coluna "Valor" para tipo numérico
        df['Valor RS'] = pd.to_numeric(df['Valor RS'], errors='coerce')
        
        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df
