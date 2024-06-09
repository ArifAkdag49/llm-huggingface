import os
import fitz  # PyMuPDF

def read_pdf(data_directory):
    pdf_text = ""
    for filename in os.listdir(data_directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(data_directory, filename)
            try:
                with fitz.open(file_path) as pdf:
                    for page_num in range(pdf.page_count):
                        page = pdf.load_page(page_num)
                        pdf_text += page.get_text()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return pdf_text

if __name__ == "__main__":
    data_directory = "./data"
    pdf_content = read_pdf(data_directory)
    print(f"PDF Content:\n{pdf_content}")
