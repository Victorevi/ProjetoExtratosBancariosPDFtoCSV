import subprocess
import sys

# Leitura OCR de PDFs
def adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida, idioma='por'):
    comando = ['ocrmypdf', '--language', idioma,  '--force-ocr', '--output-type', 'pdf']
    
    comando.extend([arquivo_entrada, arquivo_saida])
    
    subprocess.run(comando)

# Converte para TXT
def converter_pdf_para_txt(arquivo_entrada, arquivo_saida_txt, layout, raw):
    comando = ['pdftotext']

    if layout is True:
        comando.append('-layout')
    if raw is True:
        comando.append('-raw')

    comando.extend([arquivo_entrada, arquivo_saida_txt])
    subprocess.run(comando)
    print("sucesso!")

# Seleciona tipo de documento
def switch_case(tipo):
    match tipo:
        case 0:
            layout = True
            raw = True
            converter_pdf_para_txt(arquivo_entrada, arquivo_saida_txt, layout, raw)
        case 1:
            layout = True
            raw = False
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr)
            converter_pdf_para_txt(arquivo_saida_ocr, arquivo_saida_txt, layout, raw)
        case 2:
            layout = True
            raw = True
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr)
            converter_pdf_para_txt(arquivo_saida_ocr, arquivo_saida_txt, layout, raw)
        case _:
            raise ValueError("Tipo inválido!")


arquivo_entrada = sys.argv[1]
prefixo_saida = sys.argv[2]
arquivo_saida_ocr = prefixo_saida + '_ocr.pdf'
arquivo_saida_txt = prefixo_saida + '.txt'

'''
Tipos:
0 Geral
1 Santander
2 City
'''

tipo = int(sys.argv[3])
switch_case(tipo)

'''
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/ItauAbril2023.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/ItauAbril2023" "0"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/santander.pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander1" "1"
python PdfToTXT.py "C:/Users/vbarbosa/Downloads/docs bancarios/202402 - CITIBANK_90015799 Extrato de Operações (1).pdf" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202402 - CITIBANK_90015799 Extrato de Operações (1)1" "2"
'''