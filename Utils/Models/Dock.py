import re
import pandas as pd

def Dock(csv_path, texto):
    # Padrão regex
    padrao = r"^(.+)\n(\d{2}/\d{2}/\d{4})+[\d:-]+(\w+)+([-+]+[.\d,]*,\d{2}\b)+\n+([\w\d./-]+)+"
    padrao_saldo_final = r".+Dock.+à(.+)\n\n.+\n\n.+\n\n.+\n\n.+\n\n.+R[S$]+(.+)"

    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)
    matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Descrição', 'Status', 'Valor']

    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []
        for match in matches:
            descricao = match[0]+match[4]
            status = match[2][:-2]
            matches_corpo_ordenados = [match[1], descricao, status, match[3]]
            matches_ordenados.append(matches_corpo_ordenados)

        for match in matches_saldo_final:
            match_saldo_final = [match[0], 'Saldo final', '', match[1]]
            matches_ordenados.append(match_saldo_final)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

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
        
        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")
    
    return df