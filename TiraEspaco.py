txt_path = "C:/Users/vbarbosa/Downloads/docs bancarios/Script/202403.txt"

with open(txt_path, 'r', encoding='utf-8') as file:
    # Remover espaços em branco de cada linha e juntar as linhas em uma única string
    linhas = []
    linha_anterior_vazia = False
    for linha in file:
        linha_stripped = linha.strip()
        if linha_stripped:
            linhas.append(linha_stripped.replace(" ", ""))
            linha_anterior_vazia = False
        elif not linha_anterior_vazia:
            linhas.append('')
            linha_anterior_vazia = True

# Salvar o texto processado em um novo arquivo
with open(txt_path, 'w', encoding='utf-8') as file:
    file.writelines('\n'.join(linhas))
    print("Texto processado e salvo com sucesso!")