import re
import pandas as pd

def PinbankExtratoContaPL(csv_path, texto):
    # Padrão regex
    padrao = r"^([\d/]+)+ +[\d:]* *([\w $]+)+ ([\d.,-]+) *(\w+)*"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Descrição', 'Valor', 'Operador']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('.', '').replace(',', '')

            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if row['Operador'].startswith('D'):
                cleaned_value = '-' + cleaned_value[0:]

            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                # Atualizar o valor na coluna 'Valor'
                df.at[index, 'Valor'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor'] = ''
        
        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df