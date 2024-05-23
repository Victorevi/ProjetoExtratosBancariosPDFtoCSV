import re
import pandas as pd

def CitiExtratoCC(csv_path, texto):
    # Padrão regex
    padrao = r"^(\d{2}/\d{2}/\d{4})+\s+(\d{2}/\d{2}/\d{4})*\s*(\d{4})*\s*([ \w\d./-]+)\s+([-.\d,]*,\d{2}\b-*)+"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data Process', 'Data Valor', 'Código', 'Descrição', 'Valor']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        def limpar_e_preencher_arrays(array):
            # Remover arrays que contenham apenas strings vazias
            array = [subarray for subarray in array if not all(item == '' for item in subarray)]

            # Preencher o primeiro elemento de cada array com o elemento anterior
            for i in range(1, len(array)):
                if array[i][0] == '':
                    array[i][0] = array[i-1][0]

            return array

        macthes_formatados = limpar_e_preencher_arrays(matches)

        df = pd.DataFrame(macthes_formatados, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('.', '').replace(',', '').replace('--','-')
            
            try:
                # Tentar converter para float
                float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                # Atualizar o valor na coluna 'Valor'
                df.at[index, 'Valor'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                print(cleaned_value)
                print("valor não encontrado")
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor'] = ''
        
        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

    return df