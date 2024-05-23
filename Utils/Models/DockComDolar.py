import re
import pandas as pd

def DockComDolar(csv_path, texto):
    # Padrão regex
    padrao1 = r"^\n([\d/]+)+[\d:;-]+(.+)[Rr]+[sS$]+([-+.\d,]+)+]*[|]*[Uu]+[Ss$]+[Ss$]+([-+.\d,]+)"
    padrao2 = r"^(.+)\n([\d/]+)+[\d;:-]+(\w+)+[Rr]+[sS$]+([-+.\d,]+)+]*[|]*[Uu]+[Ss$]+[Ss$]+([-+.\d,]+)\n(\w+)"
    padrao_saldo_final = r".+Dock.+à(.+)\n\n.+\n\n.+\n\n.+\n\n.+\n.+R[S$]+(.+)\n"

    # Procurando por todas as correspondências no texto
    matches1 = re.findall(padrao1, texto, re.MULTILINE)
    matches2 = re.findall(padrao2, texto, re.MULTILINE)
    matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas1 = ['Data', 'Descrição', 'Valor', 'Valor USS']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches1 and matches2:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []
        for match in matches1:
            matches_corpo_ordenados = [match[0], match[1], match[2], match[3]]
            matches_ordenados.append(matches_corpo_ordenados)

        for match in matches2:
            descricao = match[0]+match[5]+match[2]
            matches_corpo_ordenados = [match[1], descricao, match[3], match[4]]
            matches_ordenados.append(matches_corpo_ordenados)

        for match in matches_saldo_final:
            match_saldo_final = [match[0], 'Saldo final', '', match[1]]
            matches_ordenados.append(match_saldo_final)

        df = pd.DataFrame(matches_ordenados, columns=colunas1)

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
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor'] = ''

            # Iterar sobre as células da planilha para limpar os valores
            for index, row in df.iterrows():
                # Remover pontos e vírgulas
                cleaned_value = str(row['Valor USS']).replace('.', '').replace(',', '').replace('--','-')
                
                try:
                    # Tentar converter para float
                    float_value = round(float(cleaned_value[:-2] + '.' + cleaned_value[-2:]), 2)
                    # Atualizar o valor na coluna 'Valor'
                    df.at[index, 'Valor USS'] = float_value
                # Tratar casos onde a conversão falha
                except ValueError:
                    print(cleaned_value)
                    print("valor não encontrado")
                    # Atribuir um valor padrão ou NaN para valores inválidos
                    df.at[index, 'Valor USS'] = ''
            
        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        # Converter a coluna "Valor" para tipo numérico
        df['Valor USS'] = pd.to_numeric(df['Valor USS'], errors='coerce')

        # Ordenar o DataFrame pela coluna 'Data'
        df = df.sort_values(by='Data')  # Ordenando o DataFrame pela coluna 'Data'

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")
    
    return df