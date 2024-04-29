import pandas as pd
import os
import sys
'''
Python A.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander.csv" "BB"
Python A.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Dock.csv" "w"
'''
# Carregar o arquivo CSV
caminho_arquivo = sys.argv[1]
tipo = sys.argv[2]
dados = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8-sig')

def padroniza_docs(mapeamento_colunas, csv_path):
    # Dividir o caminho do arquivo em nome e extensão
    nome_arquivo, extensao = os.path.splitext(csv_path)
    
    # Adicionar "_MID" antes da extensão
    arquivo_final = nome_arquivo + "_MID" + extensao

    # Definir a ordem padrão das colunas
    padrao_colunas = ['Data', 'Tipo', 'Valor', 'Descricao']

    # Criar um DataFrame vazio com as colunas na ordem desejada
    dados_reordenados = pd.DataFrame(columns=padrao_colunas)

    # Preencher as colunas reordenadas com os dados originais na ordem padrão
    for coluna_padrao in padrao_colunas:
        if coluna_padrao in mapeamento_colunas.values():
            coluna_original = next((col for col, mapped_col in mapeamento_colunas.items() if mapped_col == coluna_padrao), None)
            if coluna_original:
                if coluna_padrao == 'Data':
                    dados_reordenados[coluna_padrao] = dados[coluna_original].str.replace('/', '-').str.replace('\\', '-')
                else:
                    dados_reordenados[coluna_padrao] = dados[coluna_original]
            else:
                dados_reordenados[coluna_padrao] = None
        else:
            dados_reordenados[coluna_padrao] = None

    # Salvar o novo DataFrame em um novo arquivo CSV
    dados_reordenados.to_csv(arquivo_final, index=False, sep=';', encoding='utf-8-sig')
    print("Arquivo padronizado salvo com sucesso!")

# Mapear as colunas do arquivo original para as colunas na ordem padrão
match tipo:
    case "BancoDoBrasilEmpresaExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor RS': 'Valor',
        'Documento': 'Descricao' 
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "BradescoNetEmpresaExtratoMensalPPeriodo":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor',
        'Documento': 'Descricao' 
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
        
    case "BS2ExtratoEmpresas":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
        
    case "C6ExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Documento': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "CaixaExtratoPPeriodo":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor': 'Valor',
        'Nº Documento': 'Descricao' 
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
        
    case "CitiExtratoConta":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Referências': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
        
    case "CitiExtratoC/C":
        mapeamento_colunas = {
        'Data Valor': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Código': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "CitiExtratoC/IAuto":
        mapeamento_colunas = {
        'Data Valor': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Detalhes': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "Dock":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor',
        'Valor RS': 'Valor',
        'Status': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "ItauBBA":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
      
    case "ItauExtratoC/C-A/A":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
  
    case "OriginalExtratoConta":
        mapeamento_colunas = {
        'Data': 'Data',
        'Lançamento': 'Tipo',
        'Valor': 'Valor',
        'Descrição': 'Descricao'
        }
        
        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "PinbankExtratoContaP/L":
        mapeamento_colunas = {
        'Data': 'Data',
        'Descrição': 'Tipo',
        'Valor': 'Valor'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "SantanderExtrato":
        mapeamento_colunas = {
        'Data': 'Data',
        'Histórico': 'Tipo',
        'Valor': 'Valor',
        'Nº Documento': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)

    case "TravelexExtratoC/C":
        mapeamento_colunas = {
        'Data': 'Data',
        'Tipo': 'Tipo',
        'Valor': 'Valor',
        'Detalhes': 'Descricao'
        }

        padroniza_docs(mapeamento_colunas, caminho_arquivo)
                                  
    case _:
        raise ValueError("Tipo inválido!")