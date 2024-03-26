import subprocess

def converter_pdf_para_txt(arquivo_entrada, arquivo_saida):
    comando = ['pdftotext', '-layout', '-raw', arquivo_entrada, arquivo_saida]
    subprocess.run(comando)
    print("sucesso!")

# Exemplo de uso:
arquivo_entrada = r'C:\Users\vbarbosa\Downloads\docs bancarios\STARK IP - ITAU 14446-4.pdf'
arquivo_saida_txt = r'C:\Users\vbarbosa\Downloads\docs bancarios\Script\STARK IP - ITAU 14446-4.txt'
converter_pdf_para_txt(arquivo_entrada, arquivo_saida_txt)
