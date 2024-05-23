import subprocess
import re

# Leitura OCR de PDFs
def adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida, force_ocr, idioma='por'):
    comando = ['ocrmypdf','--language', idioma, '--output-type', 'pdf', '--rotate-pages']
    
    if force_ocr is True:
        comando.append('--force-ocr')

    comando.extend([arquivo_entrada, arquivo_saida])
    
    subprocess.run(comando)

# Converte para TXT
def converter_pdf_para_txt(tipo, arquivo_entrada, prefixo_saida, arquivo_saida_txt, layout, raw, padrao='UTF-8'):
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
                padrao_re = r"(\d{16})[]|/ ]*([\w\s./\-]*)[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*(\d{2}/\d{2}/\d{4})[]|/ ]*([\w\s./\-]*)[]|/ ]* ([-.\d,]+,\d{3}\b-*|[-.\d,]+,\d{2}\b-*)[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))[]|/ ]*([-.\d,\d{2}]*(?=))"

                # Procurando por todas as correspondências no texto
                matches = re.findall(padrao_re, arquivo_txt.read(), re.MULTILINE)
                if matches:
                    print("Arquivo extraído com sucesso!")
                else:
                    print("O arquivo extraído está vazio ou não contém texto.")
                    tipo = 2
                    PdfToTxt(arquivo_entrada, prefixo_saida, tipo)

            else:
                print("Arquivo extraído com sucesso!")

        else:
            if tipo == 1:
                print("O arquivo extraído está vazio ou não contém texto.")
                tipo = 3
                PdfToTxt(arquivo_entrada, prefixo_saida, tipo)
            if tipo == 0:
                print("O arquivo extraído está vazio ou não contém texto.")
                tipo = 2
                PdfToTxt(arquivo_entrada, prefixo_saida, tipo)

# Seleciona tipo de documento
def PdfToTxt(arquivo_entrada, prefixo_saida, tipo):
    # Imputs
    arquivo_saida_ocr = prefixo_saida + '_ocr.pdf'
    arquivo_saida_txt = prefixo_saida + '.txt'
    tipo = int(tipo)

    match tipo:
        case 0:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 1:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 2:
            layout = True
            raw = True
            force_ocr = True
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 3:
            layout = True
            raw = False
            force_ocr = False
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 4:
            layout = True
            raw = False
            force_ocr = True
            adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida_ocr, force_ocr)
            converter_pdf_para_txt(tipo, arquivo_saida_ocr, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 5:
            layout = True
            raw = False
            converter_pdf_para_txt(tipo, arquivo_entrada, prefixo_saida, arquivo_saida_txt, layout, raw)
        case 6:
            layout = True
            raw = True
            converter_pdf_para_txt(tipo, arquivo_entrada, prefixo_saida, arquivo_saida_txt, layout, raw)
        case _:
            raise ValueError("Tipo inválido!")

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