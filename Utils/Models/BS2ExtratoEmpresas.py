import re
import pandas as pd

def BS2ExtratoEmpresas(csv_path, texto):
    # Padrão regex
    padrao = r"(\d{2}/\d{2}/\d{4}) ([\w\d./ ]+-*[\w\d./ ]+) ([R$ \d,.-]+,\d{2}\b)"
    padraoSaldoInicial = r"(Extraído em )(.+)|(Saldo Inicial) ([ R$S\d,.-]+,\d{2})+"
    padraoSaldoFinal = r"(Saldo Final ).+ ([\d,.-]+,\d{2})+"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    matchSaldoInicial = re.findall(padraoSaldoInicial, texto, re.MULTILINE)
    matchSaldoFinal = re.findall(padraoSaldoFinal, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Descrição', 'Valor', 'Saldo']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in matchSaldoInicial:
            matches_saldo_inicial_ordenado = [match[1], match[2], '', match[3]]
            matches_ordenados.append(matches_saldo_inicial_ordenado)

        for match in matches:
            matches_ordenado = [match[0], match[1], match[2], '']
            matches_ordenados.append(matches_ordenado)

        for match in matchSaldoFinal:
            matches_saldo_final_ordenado = ['', match[0], '', match[1]]
            matches_ordenados.append(matches_saldo_final_ordenado)

        def limpar_e_preencher_arrays(array):
            # Remover arrays que contenham apenas strings vazias
            array = [subarray for subarray in array if not all(item == '' for item in subarray)]

            # Preencher o primeiro elemento de cada array com o elemento anterior
            for i in range(1, len(array)):
                if array[i][0] == '':
                    array[i][0] = array[i-1][0]

            return array
        
        matches_ordenados = limpar_e_preencher_arrays(matches_ordenados)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('R$', '').replace('.', '').replace(',', '')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if cleaned_value.startswith('-') or cleaned_value.startswith('--') :
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

        # Converter a coluna "Valor" e "Saldo" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['Saldo'] = pd.to_numeric(df['Saldo'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df