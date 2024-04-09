import subprocess
import sys
import os
import time
import re

def limpa_caracteres(string):
    # Define a expressão regular para encontrar caracteres não ASCII
    padrao = re.compile(r'[^\x00-\x7F]+')
    # Substitui os caracteres não ASCII por uma string vazia
    string_limpa = padrao.sub('', string)
    return string_limpa

arquivo_entrada = sys.argv[1]
caminho_saida = limpa_caracteres(sys.argv[2])
tipo = sys.argv[3]
arquivo_pdf = arquivo_entrada + '.pdf'
arquivo_txt = caminho_saida + '.txt'
arquivo_csv = caminho_saida + '.xlsx'

match tipo:
    case "Banco do Brasil":
        classificacao = '0'
    case "Bradesco":
        classificacao = '0'
    case "BS2":
        classificacao = '0'
    case "C6":
        classificacao = '0'
    case "Caixa":
        classificacao = '0'
    case "Itau":
        classificacao = '0'
    case "Original":
        classificacao = '0'
    case "Travelex":
        classificacao = '0'
    case "City":
        classificacao = '2'
    case "CityLegivel":
        classificacao = '0'
    case "Santander":
        classificacao = '1'                          
    case _:
        raise ValueError("Tipo inválido!")

def chamar_script(script):
    try:
        subprocess.Popen(script, shell=True).wait()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao chamar o script {script}: {e}")

def main(tipo):
    # Mudar o diretório de trabalho para onde os scripts estão localizados
    caminho_scripts = r"C:\Users\vbarbosa\Documents\Scripts\Python\ProjetoExtratosBancariosPDFtoXLSX\ProjetoExtratosBancariosPDFtoXLSX"
    os.chdir(caminho_scripts)
    
    script_pdf = f'python PdfToTxt.py "{arquivo_pdf}" "{caminho_saida}" "{classificacao}"'
    # Chama o primeiro script
    chamar_script(script_pdf)

     # Aguarda até que o arquivo de texto seja gerado pelo primeiro script
    while not os.path.exists(arquivo_txt):
        time.sleep(1)

    if tipo == "CityLegivel":
        tipo = "City"

    script_txt = f'python TxtToXlsx.py "{arquivo_txt}" "{arquivo_csv}" "{tipo}"'
    # Chama o segundo script
    chamar_script(script_txt)

main(tipo)
'''
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/aextrato cons Itau 10704-5 agosto" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/aextrato cons Itau 10704-5 agosto" "Itau"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/caixa 254-2 01 a 15-07" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa 254-2 01 a 15-07" "Caixa"

python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/Banco do Brasil janeiro 2022  cc 51734-8" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Banco do Brasil janeiro 2022  cc 51734-8" "Banco do Brasil"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/29012024-Extrato BB (parcial)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato BB (parcial)" "Banco do Brasil"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/Bradesco dez" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez" "Bradesco"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/29012024-Extrato Bradesco (parcial)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/29012024-Extrato Bradesco (parcial)" "Bradesco"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/BS2 887946-0" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/BS2 887946-0" "BS2"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/c6" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/c6" "C6"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - C6_42457718" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - C6_42457718" "C6"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/caixa292-5 - julho-22 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/caixa292-5 - julho-22 (1)" "Caixa"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de OperaÃ§Ãµes (1)" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/202401 - 90016495 - APLICAÇÃO CDB - Extrato de posição" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202401 - 90016495 - APLICAÇÃO CDB - Extrato de posição" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_9016495 Extrato de Operações 1" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_9016495 Extrato de Operacoes 1" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações 1" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de Operacoes 1" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_090034479 Extrato de Operações (2)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_090034479 Extrato de Operações (2)" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90015799" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90015799" "City"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90016495" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90016495" "CityLegivel"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90034479" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90034479" "CityLegivel"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90034479 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operações.90034479 (1)" "CityLegivel"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90016495 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operações.90016495 (1)" "CityLegivel"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de operações.90015799 (1)" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de operações.90015799 (1)" "CityLegivel"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/ItauAbril2023" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ItauAbril2023" "Itau"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/Original Fev" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev" "Original"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/santander" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander" "Santander"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - SANTANDER 13006763-2" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - SANTANDER 13006763-2" "Santander"
python ConversãoPdfToXlsx.py "C:/Users/vbarbosa/Downloads/docs bancarios/travelex" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/travelex" "Travelex"
'''


'''
Ajustes necessários, e ajustar os itens 80/81/82, adicionar coluna saldo
Pontos a melhorar, montar um padrão de saida de arquivo XLSX, limpar os arquivos criados no percurso que não são o produto final

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