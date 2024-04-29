import subprocess
import sys
import re

# Leitura OCR de PDFs
def adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida, force_ocr, idioma='por'):
    comando = ['ocrmypdf','--language', idioma, '--output-type', 'pdf', '--rotate-pages']
    
    if force_ocr is True:
        comando.append('--force-ocr')

    comando.extend([arquivo_entrada, arquivo_saida])
    
    subprocess.run(comando)

# Converte para TXT
def converter_pdf_para_txt(tipo, arquivo_entrada, arquivo_saida_txt, layout, raw, padrao='UTF-8'):
    comando = ['pdftotext', '-enc', padrao]

    if layout is True:
        comando.append('-layout')
    if raw is True:
        comando.append('-raw')

    comando.extend([arquivo_entrada, arquivo_saida_txt])
    subprocess.run(comando)
    
    # Verifica se há texto dentro do arquivo
    with open(arquivo_saida_txt, 'r', encoding=padrao) as arquivo_txt:
        if arquivo_txt.read().strip():
            if tipo == 6:
                # Padrão regex
                padrao = r"(\d{16})[]|/ ]*([\w\s./\-]*)[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*([\w\s./\-]*)[]|/ ]* ([-.\d,]+,\d{3}\b-*|[-.\d,]+,\d{2}\b-*)[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))"

                # Procurando por todas as correspondências no texto
                matches = re.findall(padrao, arquivo_txt.read(), re.MULTILINE)
                if matches:
                    print("Arquivo extraído com sucesso!")
                else:
                    print("O arquivo extraído está vazio ou não contém texto.")
                    tipo = 2
                    switch_case(tipo)

            else:
                print("Arquivo extraído com sucesso!")
                
        else:
            if tipo == 1:
                print("O arquivo extraído está vazio ou não contém texto.")
                tipo = 3
                switch_case(tipo)
            else:
                print("O arquivo extraído está vazio ou não contém texto.")
                tipo = 2
                switch_case(tipo)

# Seleciona tipo de documento
def switch_case(tipo):
    match tipo:
        case 0:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, arquivo_saida_txt, layout, raw)
        case 1:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, arquivo_saida_txt, layout, raw)
        case 2:
            layout = True
            raw = True
            force_ocr = True
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, arquivo_saida_txt, layout, raw)
        case 3:
            layout = True
            raw = False
            force_ocr = False
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, arquivo_saida_txt, layout, raw)
        case 4:
            layout = True
            raw = False
            force_ocr = True
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, arquivo_saida_txt, layout, raw)
        case 5:
            layout = True
            raw = False
            converter_pdf_para_txt(tipo, arquivo_entrada, arquivo_saida_txt, layout, raw)
        case 6:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, arquivo_saida_txt, layout, raw)
        case _:
            raise ValueError("Tipo inválido!")

# Imputs
arquivo_entrada = sys.argv[1]
prefixo_saida = sys.argv[2]
arquivo_saida_girado = prefixo_saida+ '_girado.pfd'
arquivo_saida_ocr = prefixo_saida + '_ocr.pdf'
arquivo_saida_txt = prefixo_saida + '.txt'
tipo = int(sys.argv[3])

'''
Tipos:
0 Geral
1 Santander
2 OCR
3 santader ocr
4 dock
5 Itau BBA
6 citi
'''

switch_case(tipo)

'''

python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - CITIBANK 086326376 Escrow - Brasília.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - CITIBANK 086326376 Escrow - Brasilia" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/santander.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander1" "1"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações (1).pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de Operacoes (1)1" "2"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK- Extrato de Operações.90016495.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK- Extrato de Operacoes 90016495" "2"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/20240131 - C6_42457718.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/20240131 - C6_42457718" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/dock.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Dock" "4"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/PINBANK 00190465-0.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/PINBANK 00190465-0" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK_90015799.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK_90015799" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/CITIBANK 9003447-9 - Aplicação Sweep.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/CITIBANK 9003447-9 - Aplicacao Sweep" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/ITAÚ_5786-2.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ITAu_5786-2" "0"
'''