import re
import pandas as pd

def ItauBBA(csv_path, texto):
    # Padrão regex
    padrao = r"^*(\d{2} */ *\w{3})+ +(.+)\s+(-*[.\d,]+,\d{2})+"
    
    # Procurando por todas as correspondências no texto
    matches = re.findall(padrao, texto, re.MULTILINE)

    # Define padrão de colunas
    colunas = ['Data', 'Lançamento', 'Valor']
    
    # Pega ano
    regex_ano = r"(lançamentos período: )+.+[/]+(\d+)"
    pega_ano = re.search(regex_ano, texto).group(2)

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

    return df