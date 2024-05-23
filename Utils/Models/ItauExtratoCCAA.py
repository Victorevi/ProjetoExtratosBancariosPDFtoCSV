import re
import pandas as pd

def ItauExtratoCCAA(csv_path, texto):
    # Padrão regex
    padraoCabecalho = r"(pela Bolsa de Valores )+(\d{2}/\d{2})+([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(D = débito a compensar )+(\d{2}/\d{2})+([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(G = aplicação programada )+(\d{2}/\d{2})*([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))|(P = poupança automática )(\d{2}/\d{2})*([ \w\d./-]*(?=)) ([-.\d,\d{2}]*(?=))"
    padraoCorpo = r"^^(\d{2}/\d{2})*(.+) ([-.\d,]+,\d{2}\b-*) *([-.\d,]+,\d{2}\b-*)*"

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

    regex_ano = r"(extrato mensal ag ).+(\d{4}) +"
    pega_ano = re.search(regex_ano, texto).group(2)

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
        for index, row in df.iterrows():
            data = str(df.at[index, 'Data'])
            ano = f"-{pega_ano}"
            # Atualizar o valor na coluna 'Valor'
            df.at[index, 'Data'] = f"{data}{ano}"

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
    
    return df