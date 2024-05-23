import re
import pandas as pd

def OriginalExtratoConta(csv_path, texto):
    # Padrão regex
    padrao = r"([\w\d./ -]*)\n(\d{2}/\d{2}/\d{4}) (\w+) ([+-]* [R$]+ [-.\d,]+,\d{2}\b)\n([\w\d./ -]*)"
    padrao_saldo_final =r"Saldo em conta\n(.+)R[S$]+(.+)\n(.+)"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Lançamento', 'Tipo', 'Valor', 'Descrição']
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []
        for match in matches:
            match_ordenado = [match[1], match[0], match[2], match[3], match[4]]
            matches_ordenados.append(match_ordenado)
        for match in matches_saldo_final:
            matches_saldo_final = [match[0], match[2], '', match[1], '']
            matches_ordenados.append(matches_saldo_final)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('R$', '').replace('.', '').replace(',', '').replace('+', '')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if cleaned_value.startswith('-') or cleaned_value.startswith('--'):
                cleaned_value = '-' + cleaned_value[3:]
            
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