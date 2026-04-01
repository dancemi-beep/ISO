import os
import sys
import io

# Setup path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src", "engine"))

from document_generator import DocumentGenerator

def test_single_gen():
    generator = DocumentGenerator(
        template_dir="files/marked",
        output_dir="output",
        structure_file="document_structure.json"
    )
    
    test_user_data = {
        "company_name": "驗證科技",
        "company_short_name": "驗證",
        "publish_date": "2026/03/10",
        "version": "1.0.0",
        "department": "資安部",
        "doc_prefix": "TST"
    }
    
    # Test a known document that should have been encrypted
    # Example: IS-001 資訊安全政策.docx
    orig_name = "IS-001 資訊安全政策.docx"
    enc_path = os.path.join("files", "marked", orig_name + ".enc")
    
    if not os.path.exists(enc_path):
        print(f"Error: Encrypted template not found at {enc_path}")
        return

    print(f"Found encrypted template: {enc_path}")
    
    # Run generation
    # results = generator.generate_all(test_user_data)
    # Let's just test one file through generate_document directly
    output_path = os.path.join("output", "TST-001 資訊安全政策.docx")
    ok = generator.generate_document(
        os.path.join("files", "marked", orig_name),
        output_path,
        ["company_name", "publish_date"],
        test_user_data
    )
    
    if ok and os.path.exists(output_path):
        print(f"Success! Generated file: {output_path}")
        print(f"Size: {os.path.getsize(output_path)} bytes")
    else:
        print("Failed to generate document from encrypted template.")

if __name__ == "__main__":
    test_single_gen()
