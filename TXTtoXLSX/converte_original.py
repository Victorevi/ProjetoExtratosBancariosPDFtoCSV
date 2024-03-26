import sys
import re
import openpyxl

txt_path = sys.argv[1]

# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()
    
# Padrão regex
padrao = r"([\w\d./ -]*)\n(\d{2}/\d{2}/\d{4}) (\w+) ([+-])* [R$]+ ([-.\d,]+,\d{2}\b)\n([\w\d./ -]*)"

# Procurando por todas as correspondências no texto
matches = re.findall(padrao, texto)

# Se houver correspondências, escrever os dados em um arquivo XLSX
if matches:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Data', 'Lançamento', 'tipo', 'Operador', 'Valor', 'Descrição'])
    for match in matches:
        ws.append(list([match[1], match[0], match[2], match[3], match[4], match[5]]))
    
    xlsx_path = sys.argv[2]
    wb.save(xlsx_path)
    print(f"Arquivo XLSX criado com sucesso em: {xlsx_path}")
else:
    print("Nenhuma correspondência encontrada.")

#python converte_Original.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/Original Fev.xlsx"