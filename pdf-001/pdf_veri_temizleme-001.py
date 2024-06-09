import os
import fitz  # PyMuPDF

def clean_pdf_text(pdf_text):
    # Gerekirse burada PDF metni üzerinde temizlik işlemleri yapılabilir
    # Örneğin gereksiz boşlukların temizlenmesi, özel karakterlerin kaldırılması vb.
    cleaned_text = pdf_text.replace("\n", " ").strip()
    return cleaned_text

def read_and_clean_pdf(data_directory):
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
    cleaned_text = clean_pdf_text(pdf_text)
    return cleaned_text

if __name__ == "__main__":
    data_directory = "./data"
    cleaned_pdf_content = read_and_clean_pdf(data_directory)
    print(f"Cleaned PDF Content:\n{cleaned_pdf_content}")
