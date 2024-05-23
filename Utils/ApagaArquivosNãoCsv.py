import os

def deletar_arquivos_txt_e_pdf(pasta):
    # Verificar se o diretório existe
    if not os.path.isdir(pasta):
        print(f'O diretório {pasta} não existe.')
        return
    
    # Listar todos os arquivos na pasta
    arquivos = os.listdir(pasta)
    
    # Iterar sobre os arquivos e deletar os que são .txt ou .pdf
    for arquivo in arquivos:
        if arquivo.endswith('.pdf') or arquivo.endswith('.txt'):
            caminho_completo = os.path.join(pasta, arquivo)
            os.remove(caminho_completo)
            print(f'Arquivo {caminho_completo} deletado com sucesso.')