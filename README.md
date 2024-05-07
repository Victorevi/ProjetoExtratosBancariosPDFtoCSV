# Conversor de Documentos PDF para CSV

Este é um conjunto de scripts em Python para converter documentos PDF em arquivos CSV, com o objetivo de extrair e organizar informações financeiras de extratos bancários. O processo envolve a extração de texto dos PDFs, a aplicação de reconhecimento óptico de caracteres (OCR) quando necessário e a conversão dos dados extraídos para o formato CSV.

## Funcionalidades Principais

- Conversão de documentos PDF em texto utilizando a biblioteca `poppler`.
- Aplicação de OCR para documentos PDF não legíveis utilizando o `ocrmypdf`.
- Extração de informações específicas dos extratos bancários utilizando expressões regulares.
- Conversão dos dados extraídos para o formato CSV utilizando `pandas`.
- Padronização dos documentos para um formato específico.
- Exclusão dos arquivos gerados no caminho

## Scripts em funcionamento parados no desenvolvimento

- TxtToXlsx.py
- Split.py


## Requisitos

- Python 3.x
- Bibliotecas Python: pandas, poppler-utils, ocrmypdf
- Scoop para instalação: ghostscript, tesseract, poppler

"Para utilização de idiomas no tesseract utilize o tesseract-languages disponível em:
https://github.com/tesseract-ocr/tessdata_fast"

## Uso

1. Clone este repositório em sua máquina local.
2. Instale as dependências Python listadas nos requisitos.
3. Troque o caminho do script nas linhas 77 e 81 do ConversãoPdfToCsv.py

## Como Contribuir

Se você deseja contribuir para este projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua contribuição (`git checkout -b feature/SuaContribuicao`).
3. Faça suas alterações e comente-as de forma clara.
4. Faça o commit de suas alterações (`git commit -am 'Adiciona nova funcionalidade'`).
5. Envie suas alterações para o seu fork (`git push origin feature/SuaContribuicao`).
6. Crie um novo Pull Request.

## Exemplos de Uso

Aqui estão alguns exemplos de como usar os scripts para converter diferentes tipos de documentos PDF em arquivos CSV:

```bash
python ConversãoPdfToCsv.py "Caminho/Para/Seu/Arquivo" "Caminho/Para/Saída" "TipoDoDocumento"
