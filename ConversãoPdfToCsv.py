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
        processo = subprocess.Popen(script, shell=True)
        processo.wait()
        if processo.returncode != 0:
            raise subprocess.CalledProcessError(processo.returncode, script)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao chamar o script {script}: {e}")
        raise subprocess.CalledProcessError(f"Erro ao chamar o script {script}: {e}")

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