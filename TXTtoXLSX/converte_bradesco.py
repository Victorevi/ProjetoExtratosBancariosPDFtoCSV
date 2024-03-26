import sys
import re
import openpyxl

txt_path = sys.argv[1]

# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()
    
# Padrão regex
padrao = r"([\w\d./ -]*\n[\w\d./ -]*)\n(\d+) ([-.\d,]+,\d{2}\b-*) ([-.\d,]+,\d{2}\b-*)"

# Procurando por todas as correspondências no texto
matches = re.findall(padrao, texto)

# Se houver correspondências, escrever os dados em um arquivo XLSX
if matches:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Lançamento', 'Documento', 'Valor', 'Saldo'])
    for match in matches:
        ws.append(list(match))
    
    xlsx_path = sys.argv[2]
    wb.save(xlsx_path)
    print(f"Arquivo XLSX criado com sucesso em: {xlsx_path}")
else:
    print("Nenhuma correspondência encontrada.")

#python converte_bradesco.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Bradesco dez.xlsx"