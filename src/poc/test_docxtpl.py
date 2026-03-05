from docxtpl import DocxTemplate
import os

def test_docxtpl():
    template_path = "src/poc/IS-001_template_marked.docx"
    output_path = "output/IS-001_output_docxtpl.docx"
    
    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        return
        
    doc = DocxTemplate(template_path)
    
    context = {
        "company_name": "星際爭霸股份有限公司",
        "publish_date": "2026/12/31"
    }
    
    try:
        doc.render(context)
        doc.save(output_path)
        print(f"Successfully rendered with docxtpl to: {output_path}")
    except Exception as e:
        print(f"Error rendering: {e}")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
    test_docxtpl()
