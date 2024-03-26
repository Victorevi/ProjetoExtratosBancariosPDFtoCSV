import subprocess


def adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida, idioma='por'):
    comando = ['ocrmypdf', '--language', idioma,  '--force-ocr', '--output-type', 'pdf']
    
    '''if deskew:
        comando.append('--deskew')
    if clean:
        comando.append('--clean')'''
    
    comando.extend([arquivo_entrada, arquivo_saida])
    
    subprocess.run(comando)
    

# Exemplo de uso:
arquivo_entrada = r'C:\Users\vbarbosa\Downloads\docs bancarios\santander.pdf'
arquivo_saida = r'C:\Users\vbarbosa\Downloads\docs bancarios\Script\santander_ORC.pdf'
adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida)

def converter_pdf_para_txt(arquivo_entrada, arquivo_saida):
    comando = ['pdftotext', '-layout', arquivo_entrada, arquivo_saida]
    subprocess.run(comando)
    print("sucesso!")

# Exemplo de uso:
arquivo_saida_txt = r'C:\Users\vbarbosa\Downloads\docs bancarios\Script\santander_ORC.txt'
converter_pdf_para_txt(arquivo_saida, arquivo_saida_txt)
