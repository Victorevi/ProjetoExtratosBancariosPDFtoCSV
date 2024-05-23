import pandas as pd
from Utils.Models.BancoDoBrasilEmpresaExtratoCC import BancoDoBrasilEmpresaExtratoCC
from Utils.Models.BradescoNetEmpresaExtratoMensalPPeriodo import BradescoNetEmpresaExtratoMensalPPeriodo
from Utils.Models.BS2ExtratoEmpresas import BS2ExtratoEmpresas
from Utils.Models.C6ExtratoCC import C6ExtratoCC
from Utils.Models.CaixaExtratoPPeriodo import CaixaExtratoPPeriodo
from Utils.Models.CitiExtratoConta import CitiExtratoConta
from Utils.Models.CitiExtratoCC import CitiExtratoCC
from Utils.Models.CitiExtratoCIAuto import CitiExtratoCIAuto
from Utils.Models.CitiExtratoOperacoes import CitiExtratoOperacoes
from Utils.Models.Dock import Dock
from Utils.Models.DockComDolar import DockComDolar
from Utils.Models.ItauBBA import ItauBBA
from Utils.Models.ItauExtratoCCAA import ItauExtratoCCAA
from Utils.Models.OriginalExtratoConta import OriginalExtratoConta
from Utils.Models.PinbankExtratoContaPL import PinbankExtratoContaPL
from Utils.Models.SantanderExtrato import SantanderExtrato
from Utils.Models.TravelexExtratoCC import TravelexExtratoCC

#Imputs
txt_path = None
csv_path = None
tipo = None
df = None

def RemoveEspaco(txt_path):
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

    return texto

def padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado= False):
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

def TxtToCsv(txt_path, csv_path, tipo):

    # Ler o texto do arquivo 
    with open(txt_path, 'r', encoding='utf-8') as file:
        texto = file.read()
    
    # Tente encontrar todas as correspondências no texto
    # Mapear as colunas do arquivo original para as colunas na ordem padrão
    try:
        match tipo:
            case "BancoDoBrasilEmpresaExtratoC/C":
                df = BancoDoBrasilEmpresaExtratoCC(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Histórico': 'Tipo',
                'Valor RS': 'Valor',
                'lote': 'Descricao' 
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "BradescoNetEmpresaExtratoMensalPPeriodo":
                df = BradescoNetEmpresaExtratoMensalPPeriodo(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Lançamento': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Documento': 'Descricao' 
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)
            
            case "BS2ExtratoEmpresas":
                df = BS2ExtratoEmpresas(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo'
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)
            
            case "C6ExtratoC/C":
                df = C6ExtratoCC(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Operador': 'Descricao'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)
            
            case "CaixaExtratoPPeriodo":
                df = CaixaExtratoPPeriodo(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Histórico': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Nº Documento': 'Descricao' 
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)

            case "CitiExtratoConta":
                df = CitiExtratoConta(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Referências': 'Descricao'
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)

            case "CitiExtratoC/C":
                df = CitiExtratoCC(csv_path, texto)

                mapeamento_colunas = {
                'Data Valor': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Código': 'Descricao'
                }
                
                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "CitiExtratoC/IAuto":
                df = CitiExtratoCIAuto(csv_path, texto)

                mapeamento_colunas = {
                'Data Valor': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Detalhes': 'Descricao'
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)

            case "CitiExtratoOperacoes":
                CitiExtratoOperacoes(csv_path, texto)
            
            case "Dock":
                texto_dock = RemoveEspaco(txt_path)

                df = Dock(csv_path, texto_dock)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Status': 'Descricao'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)
            
            case "DockComDolar":
                texto_dock = RemoveEspaco(txt_path)

                df = DockComDolar(csv_path, texto_dock)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "ItauBBA":
                df = ItauBBA(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Lançamento': 'Tipo',
                'Valor': 'Valor'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "ItauExtratoC/C-A/A":
                df = ItauExtratoCCAA(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)
            
            case "OriginalExtratoConta":
                df = OriginalExtratoConta(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Lançamento': 'Tipo',
                'Valor': 'Valor',
                'Descrição': 'Descricao'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "PinbankExtratoContaP/L":
                df = PinbankExtratoContaPL(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Descrição': 'Tipo',
                'Valor': 'Valor'
                }

                saldo_errado = True

                padroniza_docs(mapeamento_colunas, csv_path, df, saldo_errado)

            case "SantanderExtrato":
                df = SantanderExtrato(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Histórico': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Nº Documento': 'Descricao'
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)

            case "TravelexExtratoC/C":
                df = TravelexExtratoCC(csv_path, texto)

                mapeamento_colunas = {
                'Data': 'Data',
                'Tipo': 'Tipo',
                'Valor': 'Valor',
                'Saldo': 'Saldo',
                'Detalhes': 'Descricao'
                }

                padroniza_docs(mapeamento_colunas, csv_path, df)
                                            
            case _:
                raise ValueError("Tipo inválido!")
    except Exception as e:
        # Se ocorrer algum erro, imprima a exceção
        raise ValueError(f"Nenhuma correspondência encontrada, verifique o tipo do arquivo!\nArquivo selecionado:{tipo}")