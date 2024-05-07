import sys
import re
import openpyxl

txt_path = sys.argv[1]

# Ler o texto do arquivo 
with open(txt_path, 'r', encoding='utf-8') as file:
    texto = file.read()
    
# Padrão regex
padrao = r"(\d{16})\s*[|]\s*([\w\s./\-]*)\s*[|]\s*(\d{2}/\d{2}/\d{4})\s*[|]\s*(\d{2}/\d{2}/\d{4})\s*[|]\s*(\d{2}/\d{2}/\d{4})\s*[|]\s*([\w\s./\-]*)\s+([\d,\d{3}.-]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))\s*([-.\d,\d{2}]*(?=))"

# Procurando por todas as correspondências no texto
matches = re.findall(padrao, texto)

# Se houver correspondências, escrever os dados em um arquivo XLSX
if matches:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Número da Operação', 'Título', 'Data de Início', 'Data de Vencimento', 'Data de Liquidação', 'Indexador', '(%) do Indexador', 'Taxa Original (a.a)', 'Valor Inicial da Aplicação (R$)', 'Valor Base da Aplicação Corrigido (R$)', 'Rendimento Bruto do Título (R$)', 'IOF (R$)', 'IRRF (R$)', 'Rendimento Líquido do Título (R$)', 'Valor Base de Aplicação Liquido (R$)', '% Resgate Antecipado'])
    for match in matches:
        ws.append(list(match))
    
    xlsx_path = sys.argv[2]
    wb.save(xlsx_path)
    print(f"Arquivo XLSX criado com sucesso em: {xlsx_path}")
else:
    print("Nenhuma correspondência encontrada.")
