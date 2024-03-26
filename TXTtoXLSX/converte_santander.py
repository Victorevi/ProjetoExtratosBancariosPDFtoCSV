import sys
import re
import openpyxl

txt_path = sys.argv[1]

# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()
    
# Padrão regex
padrao = r"(\d{2}/\d{2}/\d{4})\s*([\w\s\d./-]*(?=))\s*(\d{6})\s*([\d,\d{2}.-]*(?=))"

# Procurando por todas as correspondências no texto
matches = re.findall(padrao, texto)

# Se houver correspondências, escrever os dados em um arquivo XLSX
if matches:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Data', 'Histórico', 'Nº Documento', 'Valor'])
    for match in matches:
        ws.append(list(match))
    
    xlsx_path = sys.argv[2]
    wb.save(xlsx_path)
    print(f"Arquivo XLSX criado com sucesso em: {xlsx_path}")
else:
    print("Nenhuma correspondência encontrada.")

#python converte_santander.py "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander_ORC.txt" "C:/Users/vbarbosa/Downloads/docs bancarios/Script/santander_ORC.xlsx"