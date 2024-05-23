import re
import pandas as pd

def CitiExtratoOperacoes(csv_path, texto):
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

    return df