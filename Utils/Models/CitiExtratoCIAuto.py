import re
import pandas as pd

def CitiExtratoCIAuto(csv_path, texto):
    # Padrão regex
    padrao = r"^([\w\d./ -]*) ([-.\d,]+,\d{2}\b-*) *([\w\d.,:/ -]+)*\n(\d+)+\n+(\d{2}/\d{2}/\d{4})+\n+(\d{2}/\d{2}/\d{4})+\n+"
    padrao_saldos = r"Período do Extrato (.+)\nValor Total dos Créditos Valor Total dos Débitos\nSaldo Inicial Saldo Disponível Final\n.+\n([\d,.-]+,\d{2})+ ([\d,.-]+,\d{2})+\s"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    matches_saldos = re.findall(padrao_saldos, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data Valor', 'Referência Banco', 'Descrição', 'Valor', 'Saldo', 'Detalhes']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in matches_saldos:
            matches_saldo_inicial_ordenado = [match[0], '', 'Saldo Inicial', '', match[1], '']
            matches_ordenados.append(matches_saldo_inicial_ordenado)
        for match in matches:
            matches_corpo_ordenados = [match[5], match[3], match[0], match[1], '', match[2]]
            matches_ordenados.append(matches_corpo_ordenados)
        for match in matches_saldos:
            matches_saldo_final_ordenado = [match[0], '', 'Saldo Final', '', match[2], '']
            matches_ordenados.append(matches_saldo_final_ordenado)

        def limpar_arrays(array):
            # Remover arrays que contenham apenas strings vazias
            array = [subarray for subarray in array if not all(item == '' for item in subarray)]

            return array
        
        matches_ordenados = limpar_arrays(matches_ordenados)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('.', '').replace(',', '').replace('--','-')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if cleaned_value.endswith('-'):
                cleaned_value = '-' + cleaned_value[:-1]
            
            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                # Atualizar o valor na coluna 'Valor'
                df.at[index, 'Valor'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor'] = ''


            # Remover pontos e vírgulas
            cleaned_value_saldo = str(row['Saldo']).replace('.', '').replace(',', '').replace('--','-')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if cleaned_value_saldo.endswith('-'):
                cleaned_value_saldo = '-' + cleaned_value_saldo[:-1]
            
            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value_saldo[:-2] + '.' + cleaned_value_saldo[-2:]), 2)
                # Atualizar o valor na coluna 'Valor'
                df.at[index, 'Saldo'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Saldo'] = ''
        
        # Converter a coluna "Valor" e 'Saldo' para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['Saldo'] = pd.to_numeric(df['Saldo'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df