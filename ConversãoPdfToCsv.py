import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime

def limpa_caracteres(string):
    # Define a expressão regular para encontrar caracteres não ASCII
    padrao = re.compile(r'[^\x00-\x7F]+')
    # Substitui os caracteres não ASCII por uma string vazia
    string_limpa = padrao.sub('', string)
    return string_limpa

def remover_nome_arquivo(caminho_completo):
    # Obter apenas o diretório do caminho completo
    diretorio = os.path.dirname(caminho_completo)
    return diretorio

arquivo_entrada = sys.argv[1]
caminho_saida = limpa_caracteres(sys.argv[2])
tipo = sys.argv[3]
arquivo_pdf = f"{arquivo_entrada}.pdf"
arquivo_txt = f"{caminho_saida}.txt"
arquivo_csv = f"{caminho_saida}.csv"
pasta_saida = remover_nome_arquivo(arquivo_csv)

match tipo:
    case "BancoDoBrasilEmpresaExtratoC/C":
        classificacao = '0'
    case "BradescoNetEmpresaExtratoMensalPPeriodo":
        classificacao = '0'
    case "BS2ExtratoEmpresas":
        classificacao = '0'
    case "C6ExtratoC/C":
        classificacao = '0'
    case "CaixaExtratoPPeriodo":
        classificacao = '0'
    case "CitiExtratoOperacoes":
        classificacao = '6'
    case "CitiExtratoC/C":
        classificacao = '0'
    case "CitiExtratoConta":
        classificacao = '0'
    case "CitiExtratoC/IAuto":
        classificacao = '0'
    case "Dock":
        classificacao = '4'
    case "ItauExtratoC/C-A/A":
        classificacao = '0'
    case "ItauBBA":
        classificacao = '5'
    case "OriginalExtratoConta":
        classificacao = '0'
    case "PinbankExtratoContaP/L":
        classificacao = '0'
    case "SantanderExtrato":
        classificacao = '1'
    case "TravelexExtratoC/C":
        classificacao = '0'
    case _:
        raise ValueError("Tipo inválido!")

def chamar_script(script):
    try:
        subprocess.Popen(script, shell=True).wait()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao chamar o script {script}: {e}")
        logging.error(f"Erro ao chamar o script {script}: {e}")

def main(tipo):
    # Mudar o diretório de trabalho para onde os scripts estão localizados
    caminho_scripts = "C:/Users/vbarbosa/Documents/Scripts/Python/ProjetoExtratosBancariosPDFtoCSV"
    os.chdir(caminho_scripts)

    # Montar o caminho completo para o arquivo de log
    caminho_logs = 'C:/Users/vbarbosa/Documents/Scripts/Python/ProjetoExtratosBancariosPDFtoCSV/Logs'
    nome_log = f'{caminho_logs}/conversao_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    # Configurar o logger
    logging.basicConfig(filename=nome_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Adicionar logs
    logging.info(f'Iniciando conversão para o tipo: {tipo}')
    logging.info(f'Arquivo de entrada: {arquivo_entrada}')
    logging.info(f'Caminho de saída: {caminho_saida}')
    script_pdf = f'python PdfToTxt.py "{arquivo_pdf}" "{caminho_saida}" "{classificacao}"'
    # Chama o primeiro script
    chamar_script(script_pdf)

    # Aguarda até que o arquivo de texto seja gerado pelo primeiro script
    while not os.path.exists(arquivo_txt):
        time.sleep(1)

    script_txt = f'python TxtToCsv.py "{arquivo_txt}" "{arquivo_csv}" "{tipo}"'
    # Chama o segundo script
    chamar_script(script_txt)

    # Aguarda até que o arquivo de CSV seja gerado pelo primeiro script
    while not os.path.exists(arquivo_csv):
        time.sleep(1)

    script_apaga = f'python ApagaArquivosNãoCsv.py  "{pasta_saida}"'
    # Chama o segundo script
    chamar_script(script_apaga)

    # Adicionar log de conclusão
    print('Conversão concluída com sucesso!')
    logging.info('Conversão concluída com sucesso!')

main(tipo)

'''
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/aextrato cons Itau 10704-5 agosto" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/aextrato cons Itau 10704-5 agosto" "ItauExtratoC/C-A/A"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/caixa 254-2 01 a 15-07" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa 254-2 01 a 15-07" "CaixaExtratoPPeriodo"

python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Banco do Brasil janeiro 2022  cc 51734-8" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Banco do Brasil janeiro 2022  cc 51734-8" "BancoDoBrasilEmpresaExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/29012024-Extrato BB (parcial)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato BB (parcial)" "BancoDoBrasilEmpresaExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Bradesco dez" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez" "BradescoNetEmpresaExtratoMensalPPeriodo"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/29012024-Extrato Bradesco (parcial)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato Bradesco (parcial)" "BradescoNetEmpresaExtratoMensalPPeriodo"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/BS2 887946-0" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/BS2 887946-0" "BS2ExtratoEmpresas"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/c6" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/c6" "C6ExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - C6_42457718" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - C6_42457718" "C6ExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/caixa292-5 - julho-22 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa292-5 - julho-22 (1)" "CaixaExtratoPPeriodo"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de OperaÃ§Ãµes (1)" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202401 - 90016495 - APLICAÇÃO CDB - Extrato de posição" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202401 - 90016495 - APLICAÇÃO CDB - Extrato de posição" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_9016495 Extrato de Operações 1" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_9016495 Extrato de Operacoes 1" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações 1" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de Operacoes 1" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_090034479 Extrato de Operações (2)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_090034479 Extrato de Operações (2)" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90015799" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90015799" "CitiExtratoOperacoes"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90016495" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90016495" "CitiExtratoOperacoesLegivel"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90034479" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90034479" "CitiExtratoOperacoesLegivel"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90034479 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operações.90034479 (1)" "CitiExtratoOperacoesLegivel"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90016495 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operações.90016495 (1)" "CitiExtratoOperacoesLegivel"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de operações.90015799 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de operações.90015799 (1)" "CitiExtratoOperacoesLegivel"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - CITIBANK 086326376 Escrow - Brasília" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - CITIBANK 086326376 Escrow - Brasília" "CitiExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/dock" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/dock" "Dock"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/202403" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202403" "Dock"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/ItauAbril2023" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ItauAbril2023" "ItauExtratoC/C-A/A"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/Original Fev" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev" "OriginalExtratoConta"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/santander" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander" "SantanderExtrato"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - SANTANDER 13006763-2" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - SANTANDER 13006763-2" "SantanderExtrato"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/travelex" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/travelex" "TravelexExtratoC/C"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/PINBANK 00190465-0" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/PINBANK 00190465-0" "PinbankExtratoContaP/L"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK_90015799" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK_90015799" "CitiExtratoConta"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK 9003447-9 - Aplicação Sweep" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK 9003447-9 - Aplicação Sweep" "CitiExtratoC/IAuto"
python ConversãoPdfToCsv.py "C:/Users/vbarbosa/Downloads/docs bancarios/ITAÚ_99589-9" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ITAu_99589-9" "ItauBBA"
'''



'''
adicionar  o nome do arquivo nos logs e dia/tempo logging https://docs.python.org/pt-br/3/howto/logging.html
Pontos a melhorar, montar um padrão de saida de arquivo CSV, limpar os arquivos criados no percurso que não são o produto final

De-Para e quantidade de arquivos testados
Banco do Brasil(X) 2
Bradesco() Problematico 
BS2()
C6()
Caixa(X) 2
Itau (X) 2
Original() Problematico
Santander(X) 2
Travelex()
'''