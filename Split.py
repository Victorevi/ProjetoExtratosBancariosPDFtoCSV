import sys
import pypdf 

def divide_pdf(input_pdf, output_folder, output_prefix, pages_per_segment=400):
    with open(input_pdf, 'rb') as file:
        pdf_reader = pypdf .PdfReader(file)
        total_pages = len(pdf_reader.pages)

        for segment_start in range(0, total_pages, pages_per_segment):
            segment_end = min(segment_start + pages_per_segment - 1, total_pages - 1)

            pdf_writer = pypdf .PdfWriter()
            for page_num in range(segment_start, segment_end + 1):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file = output_folder + f"{output_prefix}_{segment_start + 1}-{segment_end + 1}.pdf"
            with open(output_file, 'wb') as output:
                pdf_writer.write(output)

            print(f"Segment {segment_start + 1}-{segment_end + 1} written to {output_file}")

if __name__ == "__main__":
    input_pdf = sys.argv[1]  # Primeiro argumento é o caminho do arquivo PDF
    print(input_pdf)
    output_folder = sys.argv[2]  # Segundo argumento é o caminho para a pasta de 
    print(output_folder)
    output_prefix = sys.argv[3]  # Terceiro argumento é o prefixo para os nomes dos arquivos de saída
    print(output_prefix)

    divide_pdf(input_pdf, output_folder, output_prefix)  # Segundo argumento é o caminho para a pasta de saída