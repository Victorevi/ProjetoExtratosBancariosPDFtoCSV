import subprocess


'''def adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida, idioma='por', deskew=True, clean=True):
    comando = ['ocrmypdf', '--language', idioma, '--redo-ocr',  '--output-type', 'pdf', '--image-dpi', '1000', '--clean']
    
    comando.extend([arquivo_entrada, arquivo_saida])
    
    subprocess.run(comando)'''
    

# Exemplo de uso:
arquivo_entrada = r'C:\Users\vbarbosa\Downloads\docs bancarios\travelex.pdf'
arquivo_saida = r'C:\Users\vbarbosa\Downloads\docs bancarios\Script\travelex_ORC.pdf'
#adicionar_ocr_ao_pdf(arquivo_entrada, arquivo_saida)

def converter_pdf_para_txt(arquivo_entrada, arquivo_saida):
    comando = ['pdftotext', '-layout', '-raw', arquivo_entrada, arquivo_saida]
    subprocess.run(comando)
    print("sucesso!")

# Exemplo de uso:
arquivo_saida_txt = r'C:\Users\vbarbosa\Downloads\docs bancarios\Script\travelex_ORC.txt'
converter_pdf_para_txt(arquivo_entrada, arquivo_saida_txt)
