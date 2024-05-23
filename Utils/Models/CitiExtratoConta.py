import re
import pandas as pd
import datetime

def CitiExtratoConta(csv_path, texto):
    # Padrão regex
    padrao = r"^(\d{2}/\d{2}/\d{4})+ +(\d{2}/\d{2}/\d{4})+ +([\w\d./ -]*) ([-.\d,]+,\d{2}\b-*)\n([\w\d./ -]+)+\n"
    padrao_saldo_inicial = r"Período do Extrato (.+)\nSaldo Anterior Valor Total dos Créditos Valor Total dos\nDébitos\nSaldo Contábil de\nFechamento\nSaldo de\nInvestimento\nAutomático\n.+\n.+\n([\d,.-]+,\d{2})+ ([\d,.-]+,\d{2})+ "
    padrao_saldo_final = r"Período do Extrato (.+)\nSaldo Anterior Valor Total dos Créditos Valor Total dos\nDébitos\nSaldo Contábil de\nFechamento\nSaldo de\nInvestimento\nAutomático\n.+\n.+\n([\d,.-]+,\d{2})+ ([\d,.-]+,\d{2})+ "
    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    matches_saldo_inicial = re.findall(padrao_saldo_inicial, texto, re.MULTILINE)
    matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Referências', 'Valor', 'Saldo', 'Descrição']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in matches_saldo_inicial:
            matches_saldo_inicial_ordenado = [match[0], '', '', match[1], 'Saldo Inicial']
            matches_ordenados.append(matches_saldo_inicial_ordenado)
        for match in matches:
            matches_ordenado = [match[1], match[2], match[3], '', match[4]]
            matches_ordenados.append(matches_ordenado)
        for match in matches_saldo_final:
            matches_saldo_final_ordenado = [match[0], '', '', match[2], 'Saldo Final']
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
                df.at[index, 'Valor'] = ''

            # Remover pontos e vírgulas
            cleaned_value_saldo = str(row['Saldo']).replace('R$', '').replace('.', '').replace(',', '')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if cleaned_value_saldo.startswith('-') or cleaned_value_saldo.startswith('--') :
                cleaned_value_saldo = '-' + cleaned_value_saldo[3:]
            
            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value_saldo[:-2] + '.' + cleaned_value_saldo[-2:]), 2)
                # Atualizar o Saldo na coluna 'Saldo'
                df.at[index, 'Saldo'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Saldo'] = ''

        converter_data = lambda data: datetime.datetime.strptime(data, '%m/%d/%Y').strftime('%d/%m/%Y')
        # Suponha que 'data_column' seja sua coluna de data
        df['Data'] = df['Data'].apply(converter_data)


        # Converter a coluna "Valor" e "Saldo" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['Saldo'] = pd.to_numeric(df['Saldo'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df