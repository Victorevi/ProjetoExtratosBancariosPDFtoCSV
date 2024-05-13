import sys
import re
import datetime
import pandas as pd

#Imputs
txt_path = sys.argv[1]
csv_path = sys.argv[2]
tipo = sys.argv[3]

if tipo == "Dock":
    with open(txt_path, 'r', encoding='utf-8') as file:
        # Remover espaços em branco de cada linha e juntar as linhas em uma única string
        linhas = []
        linha_anterior_vazia = False
        for linha in file:
            linha_stripped = linha.strip()
            if linha_stripped:
                linhas.append(linha_stripped.replace(" ", ""))
                linha_anterior_vazia = False
            elif not linha_anterior_vazia:
                linhas.append('')
                linha_anterior_vazia = True

    # Salvar o texto processado em um novo arquivo
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.writelines('\n'.join(linhas))
        print("Texto processado e salvo com sucesso!")


# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()

    # Variáveis da função
    matches = None
    colunas = None
    matchesCabecalho = None
    matchesCorpo = None
    ordemColunas = None
# Tente encontrar todas as correspondências no texto
try:
    match tipo:
        case "BancoDoBrasilEmpresaExtratoC/C":
            # Padrão regex
            padrao = r"([\d/+]+\d{4})+ (\d{4}) (\d{5}) (.+) +([ \d,.-]+,\d{2})\s*(\w)\s*"
            
            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            #colunas = ['Data', 'Agência Origem', 'lote', 'Histórico', 'Documento', 'Valor R$', 'Operador', 'Descrição']
            colunas = ['Data', 'Agência Origem', 'lote', 'Histórico', 'Valor RS', 'Operador']

        case "BradescoNetEmpresaExtratoMensalPPeriodo":
            # Padrão regex
            padrao = r"^(\d{2}/\d{2}/\d{4})*\s*([\w\d./:& -]*\s*[\w\d./:& -]*)\s*(\d+)*\s+([-.\d,]+,\d{2}\b-*)\s*([-.\d,]+,\d{2}\b-*)*"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Lançamento', 'Documento', 'Valor', 'Saldo']
            
        case "BS2ExtratoEmpresas":
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
            
        case "C6ExtratoC/C":
            # Padrão regex
            padrao = r"(\d{2}/\d{2}/\d{4}) (.+) ([-.\d,]+,\d{2}\b) *([CD])*"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Descrição', 'Valor', 'Operador']
            
        case "CaixaExtratoPPeriodo":
            # Padrão regex
            padrao = r"(\d{2}/\d{2}/\d{4}) (\d{6}) ([\w\d./ -]*) ([-.\d,]+,\d{2}\b-*) (\w) ([-.\d,]+,\d{2}\b-*) (\w)"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Nº Documento', 'Histórico', 'Valor', 'Operador Valor', 'Saldo', 'Operador Saldo']
            
        case "CitiExtratoOperacoes":
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
            colunas = ['Número da Operação', 'Título', 'Data de Início', 'Data de Vencimento', 'Data de Liquidação', 'Indexador', '(%) do Indexador', 'Taxa Original (a.a)', 'Valor Inicial da Aplicação (RS)', 'Valor Base da Aplicação Corrigido (RS)', 'Rendimento Bruto do Título (RS)', 'IOF (RS)', 'IRRF (RS)', 'Rendimento Líquido do Título (RS)', 'Valor Base de Aplicação Liquido (RS)', 'Tipo Bloqueio', '% Resgate Antecipado']

        case "CitiExtratoC/C":
            # Padrão regex
            padrao = r"^(\d{2}/\d{2}/\d{4})+\s+(\d{2}/\d{2}/\d{4})*\s*(\d{4})*\s*([ \w\d./-]+)\s+([-.\d,]*,\d{2}\b-*)+"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data Process', 'Data Valor', 'Código', 'Descrição', 'Valor']

        case "CitiExtratoConta":
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

        case "CitiExtratoC/IAuto":
            # Padrão regex
            padrao = r"^([\w\d./ -]*) ([-.\d,]+,\d{2}\b-*) *([\w\d.,:/ -]+)*\n(\d+)+\n+(\d{2}/\d{2}/\d{4})+\n+(\d{2}/\d{2}/\d{4})+\n+"
            padrao_saldos = r"Período do Extrato (.+)\nValor Total dos Créditos Valor Total dos Débitos\nSaldo Inicial Saldo Disponível Final\n.+\n([\d,.-]+,\d{2})+ ([\d,.-]+,\d{2})+\s"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)
            matches_saldos = re.findall(padrao_saldos, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data Valor', 'Referência Banco', 'Descrição', 'Valor', 'Saldo', 'Detalhes']

        case "Dock":
            # Padrão regex
            padrao = r"^(.+)\n(\d{2}/\d{2}/\d{4})+[\d:-]+(\w+)+([-+]+[.\d,]*,\d{2}\b)+\n+([\w\d./-]+)+"
            padrao_saldo_final = r".+Dock.+à(.+)\n\n.+\n\n.+\n\n.+\n\n.+\n\n.+R[S$]+(.+)"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)
            matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Descrição', 'Status', 'Valor']

        case "ItauExtratoC/C-A/A":
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

            regex_ano = r"(extrato mensal ag ).+(\d{4}) +"
            pega_ano = re.search(regex_ano, texto).group(2)

        case "ItauBBA":
            # Padrão regex
            padrao = r"^*(\d{2} */ *\w{3})+ +(.+)\s+(-*[.\d,]+,\d{2})+"
            
            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Lançamento', 'Valor']
            
            # Pega ano
            regex_ano = r"(lançamentos período: )+.+[/]+(\d+)"
            pega_ano = re.search(regex_ano, texto).group(2)
            
        case "OriginalExtratoConta":
            # Padrão regex
            padrao = r"([\w\d./ -]*)\n(\d{2}/\d{2}/\d{4}) (\w+) ([+-]* [R$]+ [-.\d,]+,\d{2}\b)\n([\w\d./ -]*)"
            padrao_saldo_final =r"Saldo em conta\n(.+)R[S$]+(.+)\n(.+)"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)
            matches_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Lançamento', 'Tipo', 'Valor', 'Descrição']

        case "PinbankExtratoContaP/L":
            # Padrão regex
            padrao = r"^(\d{2}/\d{2}/\d{4})+ +[\d:-]*([ \w\d./-]+)+ +[RSrsR$ ]*([.\d,]+)+ *(\w+)*\n"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Descrição', 'Valor', 'Operador']

        case "SantanderExtrato":
            # Padrão regex
            padrao = r"(?!.+SALDO ANTERIOR)(\d{2}/\d{2}/\d{4})+\s+(.+) (\d+) +([-.\d,]+,\d{2}\b) *([-.\d,]+,\d{2}\b)*\s"
            padrao_saldo_inicial = r"(.+) (SALDO ANTERIOR.*) +([-.\d,]+,\d{2})+\s"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)
            match_saldo_inicial = re.findall(padrao_saldo_inicial, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Histórico', 'Nº Documento', 'Valor', 'Saldo']

        case "TravelexExtratoC/C":
            # Padrão regex
            padrao = r"\d{2}/\d{2}/\d{4}\n(\d{2}/\d{2}/\d{4})\n\d{2}:\d{2}\n([\w\sç]*\n(?!.*LIQUIDACAO)\w*)\n([\w\s\d\n./:|-]*(?=))\b(?:Sim|Não)\b ([-.\d,\d{2}]*(?=)) ([-.\d,\d{2}]*(?=))"
            padrao_saldo_inicial = r"(.+) (Saldo Inicial) (.+)"

            # Procurando por todas as correspondências no texto
            matches = re.findall(padrao, texto, re.MULTILINE)
            match_saldo_inicial = re.findall(padrao_saldo_inicial, texto, re.MULTILINE)

            # Define padrão de colunas
            colunas = ['Data', 'Tipo', 'Detalhes', 'Valor', 'Saldo']
                                    
        case _:
            raise ValueError("Tipo inválido!")
except Exception as e:
    # Se ocorrer algum erro, imprima a exceção
    raise ValueError(f"Nenhuma correspondência encontrada, verifique o tipo do arquivo!\nArquivo selecionado:{tipo}")


if tipo == "BancoDoBrasilEmpresaExtratoC/C":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            valor = row['Valor RS']
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
                df.at[index, 'Valor RS'] = float_value
            # Tratar casos onde a conversão falha
            except ValueError:
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor RS'] = ''

        # Converter a coluna "Valor" para tipo numérico
        df['Valor RS'] = pd.to_numeric(df['Valor RS'], errors='coerce')
        
        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")
        
if tipo == "BradescoNetEmpresaExtratoMensalPPeriodo":
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

if tipo == "BS2ExtratoEmpresas":
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

if tipo == "C6ExtratoC/C":
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

if tipo == "CaixaExtratoPPeriodo":
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

if tipo == "CitiExtratoOperacoes":
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
        itera_valor('Valor Inicial da Aplicação (RS)')
        itera_valor('Valor Base da Aplicação Corrigido (RS)')
        itera_valor('Rendimento Bruto do Título (RS)')
        itera_valor('IOF (RS)')
        itera_valor('IRRF (RS)')
        itera_valor('Rendimento Líquido do Título (RS)')
        itera_valor('Valor Base de Aplicação Liquido (RS)')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        print("Nenhuma correspondência encontrada.")

if tipo == "CitiExtratoC/C":
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

if tipo == "CitiExtratoConta":
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

if tipo == "CitiExtratoC/IAuto":
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

if tipo == "Dock":
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
                print(cleaned_value)
                print("valor não encontrado")
                # Atribuir um valor padrão ou NaN para valores inválidos
                df.at[index, 'Valor'] = ''
        
        # Converter a coluna "Valor" para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV criado com sucesso em: {csv_path}")
    else:
        tipo = "Dock2"

        # Padrão regex
        padrao1 = r"^\n([\d/]+)+[\d:;-]+(.+)[Rr]+[sS$]+([-+.\d,]+)+]*[|]*[Uu]+[Ss$]+[Ss$]+([-+.\d,]+)"
        padrao2 = r"^(.+)\n([\d/]+)+[\d;:-]+(\w+)+[Rr]+[sS$]+([-+.\d,]+)+]*[|]*[Uu]+[Ss$]+[Ss$]+([-+.\d,]+)\n(\w+)"
        padrao_saldo_final = r".+Dock.+à(.+)\n\n.+\n\n.+\n\n.+\n\n.+\n.+R[S$]+(.+)\n"

        # Procurando por todas as correspondências no texto
        matches1 = re.findall(padrao1, texto, re.MULTILINE)
        matches2 = re.findall(padrao2, texto, re.MULTILINE)
        match_saldo_final = re.findall(padrao_saldo_final, texto, re.MULTILINE)

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
                    print(cleaned_value)
                    print("valor não encontrado")
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

if tipo == "ItauExtratoC/C-A/A":
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

if tipo == "ItauBBA":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        df = pd.DataFrame(matches, columns=colunas)

        # Iterar sobre as células da planilha para limpar os valores
        for index, row in df.iterrows():
            def substituir_data(data):
                # Expressão regular para encontrar o padrão "dd/Mmm"
                regex_data = r'(\d{1,2}) */+ *(\w{3})'
                
                # Função de substituição
                def substituir(match):
                    dia = match.group(1)
                    mes = match.group(2).capitalize()
                    
                    # Dicionário de mapeamento de meses abreviados para números
                    meses = {'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'}
                    # Substituir o mês abreviado pelo número correspondente
                    mes_numero = meses.get(mes)
                    
                    # Retornar a data no formato desejado
                    return f"{dia}/{mes_numero}"

                # Realizar a substituição no data
                nova_data = re.sub(regex_data, substituir, data)
                return nova_data
            
            data = substituir_data(str(df.at[index, 'Data'])) 
            data_formatada = f"{data}/{pega_ano}"
            # Atualizar o valor na coluna 'Valor'
            df.at[index, 'Data'] = data_formatada

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

if tipo == "OriginalExtratoConta":
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

if tipo == "PinbankExtratoContaP/L":
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

if tipo == "SantanderExtrato":
    # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in match_saldo_inicial:
            matches_saldo_inicial_ordenado = [match[0], match[1], '', '', match[2]]
            matches_ordenados.append(matches_saldo_inicial_ordenado)
        for match in matches:
            matches_ordenado = [match[0], match[1], match[2], match[3], match[4]]
            matches_ordenados.append(matches_ordenado)

        df = pd.DataFrame(matches_ordenados, columns=colunas)

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

if tipo == "TravelexExtratoC/C":
     # Se houver correspondências, escrever os dados em um arquivo CSV
    if matches:
        matches_ordenados = []

        for match in match_saldo_inicial:
            matches_saldo_inicial_ordenado = [match[0], match[1], '', '', match[2]]
            matches_ordenados.append(matches_saldo_inicial_ordenado)
        for match in matches:
            matches_ordenado = [match[0], match[1], match[2], match[3], match[4]]
            matches_ordenados.append(matches_ordenado)

        df = pd.DataFrame(matches_ordenados, columns=colunas)
        
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

def padroniza_docs(mapeamento_colunas, csv_path, saldo_errado= False):
    # Definir a ordem padrão das colunas
    padrao_colunas = ['Data', 'Tipo', 'Valor', 'Saldo', 'Descricao']

    # Criar um DataFrame vazio com as colunas na ordem desejada
    dados_reordenados = pd.DataFrame(columns=padrao_colunas)

    # Preencher as colunas reordenadas com os dados originais na ordem padrão
    for coluna_original, coluna_padrao  in mapeamento_colunas.items():
        dados_reordenados[coluna_padrao] = df[coluna_original]

    try:
        # Formata a coluna 'Data'        
        dados_reordenados['Data'] = dados_reordenados['Data'].apply(lambda x: x.split()[0].replace('/', '-').replace('\\', '-'))
    except:
        # Formata a coluna 'Data'        
        dados_reordenados['Data'] = dados_reordenados['Data'].apply(lambda x: x.replace('/', '-').replace('\\', '-'))

    if saldo_errado == True:
        # Identificar e mover os valores da coluna 'Valor' para a coluna 'Saldo' onde o Tipo contenha 'Saldo' ou 'S A L D O' (ignorando maiúsculas)
        dados_reordenados['Saldo'] = dados_reordenados.apply(lambda row: row['Valor'] if 'SALDO' in row['Tipo'].upper() or 'S A L D O' in row['Tipo'] else None, axis=1)
        dados_reordenados['Valor'] = dados_reordenados.apply(lambda row: None if 'SALDO' in row['Tipo'].upper() or 'S A L D O' in row['Tipo'] else row['Valor'], axis=1)

    # Lambda para verificar e preencher valores de data vazios com base nas linhas acima ou abaixo
    verifica_data_vazia_baixo = lambda data, df, indice: df.at[indice+1, 'Data'] if pd.isnull(data) or data == '' and indice < len(df) - 1 else data
    verifica_data_vazia_cima = lambda data, df, indice: df.at[indice-1, 'Data'] if pd.isnull(data) or data == '' and indice > 0 else data

    # Aplicar o lambda à coluna de Data
    dados_reordenados['Data'] = dados_reordenados.apply(lambda row: verifica_data_vazia_baixo(row['Data'], dados_reordenados, row.name), axis=1)
    dados_reordenados['Data'] = dados_reordenados.apply(lambda row: verifica_data_vazia_cima(row['Data'], dados_reordenados, row.name), axis=1)

    # Lidar com o último registro do DataFrame
    ultimo_indice = len(dados_reordenados) - 1
    if pd.isnull(dados_reordenados.at[ultimo_indice, 'Data']) or dados_reordenados.at[ultimo_indice, 'Data'] == '':
        dados_reordenados.at[ultimo_indice, 'Data'] = dados_reordenados.at[ultimo_indice - 1, 'Data']

    # Salvar o novo DataFrame em um novo arquivo CSV
    dados_reordenados.to_csv(csv_path, index=False, sep=';', encoding='utf-8-sig')
    print("Arquivo padronizado salvo com sucesso!")

# Mapear as colunas do arquivo original para as colunas na ordem padrão
match tipo:
    case "BancoDoBrasilEmpresaExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor RS': 'Valor',
        'lote': 'Descricao' 
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "BradescoNetEmpresaExtratoMensalPPeriodo":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Documento': 'Descricao' 
        }

        padroniza_docs(mapeamento_colunas, csv_path)
        
    case "BS2ExtratoEmpresas":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo'
        }

        padroniza_docs(mapeamento_colunas, csv_path)
        
    case "C6ExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Operador': 'Descricao'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "CaixaExtratoPPeriodo":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Nº Documento': 'Descricao' 
        }

        padroniza_docs(mapeamento_colunas, csv_path)
        
    case "CitiExtratoConta":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Referências': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, csv_path)
        
    case "CitiExtratoC/C":
        mapeamento_colunas = {
        'Data Valor': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Código': 'Descricao'
        }
        
        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "CitiExtratoC/IAuto":
        mapeamento_colunas = {
        'Data Valor': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Detalhes': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, csv_path)

    case "Dock":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Status': 'Descricao'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "Dock2": 
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "ItauBBA":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)
      
    case "ItauExtratoC/C-A/A":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "OriginalExtratoConta":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor',
        'Descrição': 'Descricao'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "PinbankExtratoContaP/L":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor'
        }

        saldo_errado = True

        padroniza_docs(mapeamento_colunas, csv_path, saldo_errado)

    case "SantanderExtrato":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Nº Documento': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, csv_path)

    case "TravelexExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Tipo': 'Tipo',
        'Valor': 'Valor',
        'Saldo': 'Saldo',
        'Detalhes': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, csv_path)
                                  
    case _:
        raise ValueError("Tipo inválido!")