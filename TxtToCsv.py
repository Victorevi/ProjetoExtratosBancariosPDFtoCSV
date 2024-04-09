import sys
import re
import pandas as pd

#Imputs
txt_path = sys.argv[1]
csv_path = sys.argv[2]
tipo = sys.argv[3]
'''
Tipo:
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato BB (parcial).txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato BB (parcial).csv" "Banco do Brasil"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez.csv" "Bradesco"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/BS2 887946-0.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/BS2 887946-0.csv" "BS2"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - C6_42457718.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - C6_42457718.csv" "C6"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa292-5 - julho-22 (1).txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa292-5 - julho-22 (1).csv" "Caixa"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de operaes.90015799 (1).txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de operaes.90015799 (1).csv" "City"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ItauAbril2023.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ItauAbril2023.csv" "Itau"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev.csv" "Original"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander.csv" "Santander"
python TxtToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/travelex.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/travelex.csv" "Travelex"
'''

# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()

    # Variáveis da função
    matches = None
    colunas = None
    matchesCabecalho = None
    matchesCorpo = None
    ordemColunas = None

match tipo:
    case "Banco do Brasil":
        # Padrão regex
        padrao = r"(\d{2}/\d{2}/\d{4}) (\d{4}) (\d{5}) ([\w\d/. -]+) ([\d.]+) ([ R$\d,.-]+,\d{2}\b)\s*(\w)\s*"
        
        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        #colunas = ['Data', 'Agência Origem', 'lote', 'Histórico', 'Documento', 'Valor R$', 'Operador', 'Descrição']
        colunas = ['Data', 'Agência Origem', 'lote', 'Histórico', 'Documento', 'Valor R$', 'Operador']

    case "Bradesco":
        # Padrão regex
        padrao = r"^(\d{2}/\d{2}/\d{4})*\s*([\w\d./:& -]*\s*[\w\d./:& -]*)\s*(\d+)*\s+([-.\d,]+,\d{2}\b-*)\s*([-.\d,]+,\d{2}\b-*)*"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto, re.MULTILINE)

        # Define padrão de colunas
        colunas = ['Data', 'Lançamento', 'Documento', 'Valor', 'Saldo']
        
    case "BS2":
        # Padrão regex
        padrao = r"(\d{2}/\d{2}/\d{4}) ([\w\d./ ]+-*[\w\d./ ]+) ([R$ \d,.-]+,\d{2}\b)"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Descrição', 'Valor']
        
    case "C6":
        # Padrão regex
        padrao = r"(\d{2}/\d{2}/\d{4}) ([\w\d./ -]*) (\d{12})+ ([-.\d,]+,\d{2}\b) ([CD])"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Descrição', 'Documento', 'Valor', 'Operador']
        
    case "Caixa":
        # Padrão regex
        padrao = r"(\d{2}/\d{2}/\d{4}) (\d{6}) ([\w\d./ -]*) ([-.\d,]+,\d{2}\b-*) (\w) ([-.\d,]+,\d{2}\b-*) (\w)"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Nº Documento', 'Histórico', 'Valor', 'Operador Valor', 'Saldo', 'Operador Saldo']
        
    case "City":
        # Padrão regex
        padrao_antecipada = r"(\d{16})[]|/ ]*([\w\s./\-]*)[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*([\w\s./\-]*)[]|/ ]* ([-.\d,]+,\d{3}\b-*|[-.\d,]+,\d{2}\b-*)[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*\s+(\d*)\s*([-.\d,\d{2}]*(?=))"
        padrao_liquidada = r"(\d{16})[]|/ ]*([\w\s./\-]*)[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*([\w\s./\-]*)[]|/ ]* ([-.\d,]+,\d{3}\b-*|[-.\d,]+,\d{2}\b-*)[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))"

        # Encontrar o índice do trecho "Para demais siglas, consulte as Notas"
        indice_split = texto.find("Operações Liquidadas")
        parte1 = texto[:indice_split]
        parte2 = texto[indice_split:]

        # Procurando por todas as correspondências no texto
        matches_antecipada = re.findall(padrao_antecipada, parte1, re.MULTILINE)
        matches_liquidada = re.findall(padrao_liquidada, parte2, re.MULTILINE)

        # Define padrão de colunas
        colunas = ['Número da Operação', 'Título', 'Data de Início', 'Data de Vencimento', 'Data de Liquidação', 'Indexador', '(%) do Indexador', 'Taxa Original (a.a)', 'Valor Inicial da Aplicação (R$)', 'Valor Base da Aplicação Corrigido (R$)', 'Rendimento Bruto do Título (R$)', 'IOF (R$)', 'IRRF (R$)', 'Rendimento Líquido do Título (R$)', 'Valor Base de Aplicação Liquido (R$)', 'Tipo Bloqueio', '% Resgate Antecipado']
        
    case "Itau":
        # Padrão regex
        padraoCabecalho = r"(pela Bolsa de Valores )+(\d{2}/\d{2})+([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(D = débito a compensar )+(\d{2}/\d{2})+([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(G = aplicação programada )+(\d{2}/\d{2})*([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(P = poupança automática )(\d{2}/\d{2})*([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))"
        padraoCorpo = r"^(?!.*SALDO APLIC AUT MAIS)(\d{2}/\d{2})*([\w\d.,/& -]*?) ([-.\d,]+,\d{2}\b-*) *([-.\d,]+,\d{2}\b-*)*"

        # Encontrar o índice do trecho "Para demais siglas, consulte as Notas"
        indice_split = texto.find("Para demais siglas, consulte as Notas")
        parte1 = texto[:indice_split]
        parte2 = texto[indice_split:]

        # Encontrar o índice do trecho "totalizador de aplicações automáticas entrada R$ saída R$"
        indice_split2 = parte2.find("totalizador de aplicações automáticas entrada R$ saída R$")
        parte2Usavel = parte2[:indice_split2]

        # Procurando por todas as correspondências no texto
        matchesCabecalho = re.findall(padraoCabecalho, parte1)
        matchesCorpo = re.findall(padraoCorpo, parte2Usavel, re.MULTILINE)

        # Define padrão de colunas
        colunas = ['Data', 'Descrição', 'Valor', 'Saldo']
        
    case "Original":
        # Padrão regex
        padrao = r"([\w\d./ -]*)\n(\d{2}/\d{2}/\d{4}) (\w+) ([+-]* [R$]+ [-.\d,]+,\d{2}\b)\n([\w\d./ -]*)"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Lançamento', 'Tipo', 'Valor', 'Descrição']

    case "Santander":
        # Padrão regex
        padrao = r"(\d{2}/\d{2}/\d{4})+\s+([\w\d., /-]*)\s+(\d{6}|[\w/]{6})+\s+([-.\d,]+,\d{2}\b)"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Histórico', 'Nº Documento', 'Valor']

    case "Travelex":
        # Padrão regex
        padrao = r"\d{2}/\d{2}/\d{4}\n(\d{2}/\d{2}/\d{4})\n\d{2}:\d{2}\n([\w\sç]*\n(?!.*LIQUIDACAO)\w*)\n([\w\s\d\n./:|-]*(?=))\b(?:Sim|Não)\b ([-.\d,\d{2}]*(?=)) ([-.\d,\d{2}]*(?=))"

        # Procurando por todas as correspondências no texto
        matches = re.findall(padrao, texto)

        # Define padrão de colunas
        colunas = ['Data', 'Tipo', 'Detalhes', 'Valor', 'Saldo']
                                  
    case _:
        raise ValueError("Tipo inválido!")


if tipo == "Banco do Brasil":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            valor = row['Valor R$']
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
                df.at[index, 'Valor R$'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor R$'] = ''

        # Converter a coluna "Valor" para tipo numérico
        df['Valor R$'] = pd.to_numeric(df['Valor R$'], errors='coerce')
        
        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")
        
if tipo == "Bradesco":
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

if tipo == "BS2":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

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

        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

if tipo == "C6":
    #Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)
        
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('R$', '').replace('.', '').replace(',', '')
            # Verificar se o último caractere é "-" e converter para negativo se necessário
            if row['Operador'] == "D":
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

if tipo == "Caixa":
    #Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        def itera_valor(coluna, operador):
            for index, row in df.iterrows():
                # Remover pontos e vírgulas
                cleaned_value = str(row[coluna]).replace('.', '').replace(',', '')
                # Verificar se o último caractere é "-" e converter para negativo se necessário
                if row[operador] == "D":
                    cleaned_value = '-' + cleaned_value[0:]
                
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

        itera_valor('Valor', 'Operador Valor')
        itera_valor('Saldo', 'Operador Saldo')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

if tipo == "City":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches_antecipada and matches_liquidada:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []

        for match in matches_antecipada:
            matches_antecipada_ordenados = [match[0], match[1], match[2], match[3], '', match[4], match[5], match[6], match[7], match[8], match[9], match[10], match[11], match[12], match[13], match[14], match[15]]
            matches_ordenados.append(matches_antecipada_ordenados)

        for match in matches_liquidada:
            matches_liquidada_ordenados = [match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8], match[9], match[10], match[11], match[12], match[13], match[14], '', match[15]]
            matches_ordenados.append(matches_liquidada_ordenados)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

        def itera_valor(coluna):
            for index, row in df.iterrows():
                # Remover pontos e vírgulas
                cleaned_value = str(row[coluna]).replace('.', '').replace(',', '')
                # Verificar se o último caractere é "-" e converter para negativo se necessário
                if cleaned_value.startswith('-') or cleaned_value.startswith('--'):
                    cleaned_value = '-' + cleaned_value[3:]
                
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

        # Iterar sobre as células da planilha para limpar os valores
        itera_valor('Valor Inicial da Aplicação (R$)')
        itera_valor('Valor Base da Aplicação Corrigido (R$)')
        itera_valor('Rendimento Bruto do Título (R$)')
        itera_valor('IOF (R$)')
        itera_valor('IRRF (R$)')
        itera_valor('Rendimento Líquido do Título (R$)')
        itera_valor('Valor Base de Aplicação Liquido (R$)')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

if tipo == "Itau":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matchesCabecalho and matchesCorpo:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []

        for match in matchesCabecalho:
            matches_cabecalho_ordenados1 = [match[1], match[2], match[3], '']
            matches_cabecalho_ordenados2 = [match[5], match[6], match[7], '']
            matches_cabecalho_ordenados3 = ['', match[10], match[11], '']
            matches_cabecalho_ordenados4 = ['', match[14], match[15], '']
            matches_ordenados.append(matches_cabecalho_ordenados1)
            matches_ordenados.append(matches_cabecalho_ordenados2)
            matches_ordenados.append(matches_cabecalho_ordenados3)
            matches_ordenados.append(matches_cabecalho_ordenados4)

        for match in matchesCorpo:
            matches_corpo_ordenados = [match[0], match[1], match[2], match[3]]
            matches_ordenados.append(matches_corpo_ordenados)

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

        def itera_valor(coluna):
            for index, row in df.iterrows():
                # Remover pontos e vírgulas
                cleaned_value = str(row[coluna]).replace('.', '').replace(',', '')
                # Verificar se o último caractere é "-" e converter para negativo se necessário
                if cleaned_value.endswith('-'):
                    cleaned_value = '-' + cleaned_value[:-1]
                
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
        
        # Iterar sobre as células da planilha para limpar os valores
        itera_valor('Valor')
        itera_valor('Saldo')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")


if tipo == "Original":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        # Reorganizar a ordem das colunas das correspondências
        matches_ordenados = []
        for match in matches:
            match_ordenado = [match[1], match[0], match[2], match[3], match[4]]
            matches_ordenados.append(match_ordenado)

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
    
if tipo == "Santander":
     # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            # Remover pontos e vírgulas
            cleaned_value = str(row['Valor']).replace('.', '').replace(',', '')

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

if tipo == "Travelex":
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
