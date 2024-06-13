from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_pdf_texts(pdf_file):
    reader = PdfReader(pdf_file)
    pdf_texts = [p.extract_text().strip() for p in reader.pages if p.extract_text()]
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""], chunk_size=1000, chunk_overlap=0)
    character_split_texts = character_splitter.split_text('\n\n'.join(pdf_texts))
    return clean_text_list(character_split_texts)

def clean_text_list(text_list):
    cleaned_texts = []
    for text in text_list:
        text = text.replace('\t', ' ').replace('\n', ' ')
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        cleaned_texts.append(cleaned_text)
    return cleaned_texts
