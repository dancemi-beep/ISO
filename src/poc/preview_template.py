import docx

def preview_docx(file_path):
    doc = docx.Document(file_path)
    print(f"--- 預覽 {file_path} ---")
    for i, para in enumerate(doc.paragraphs[:20]):
        if para.text.strip():
            print(f"Line {i}: {para.text}")

if __name__ == "__main__":
    preview_docx("src/poc/IS-001_template.docx")
