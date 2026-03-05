import os
import json
from docxtpl import DocxTemplate

class DocumentGenerator:
    def __init__(self, template_dir, output_dir, structure_file):
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.structure_file = structure_file
        
        with open(self.structure_file, 'r', encoding='utf-8') as f:
            self.structure = json.load(f)
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_document(self, template_path, output_path, variables, user_data):
        """Generate a single document by replacing variables using docxtpl."""
        if not template_path.endswith('.docx'):
            print(f"Skipping non-docx file (currently unsupported by DocxTemplate): {template_path}")
            return
            
        try:
            doc = DocxTemplate(template_path)
            
            # Prepare context dictionary based on expected variables
            # docxtpl uses Jinja2 syntax natively, so the word template should have {{ variable_name }}
            # For this engine, we directly pass the user_data that matches the required variables.
            # We filter only the required variables for this document, but passing all user_data is also fine.
            context = {var: user_data.get(var, f"[Missing: {var}]") for var in variables}
            
            # Render context into the document
            doc.render(context)
            
            doc.save(output_path)
            print(f"Generated: {output_path}")
            
        except Exception as e:
            print(f"Error processing {template_path}: {e}")

    def generate_all(self, user_data):
        """Iterate through the structure and generate all documents."""
        for family, files in self.structure.items():
            for file_info in files:
                filename = file_info['filename']
                variables = file_info.get('variables', [])
                
                template_path = os.path.join(self.template_dir, filename)
                output_path = os.path.join(self.output_dir, filename)
                
                if os.path.exists(template_path):
                    self.generate_document(template_path, output_path, variables, user_data)
                else:
                    print(f"Warning: Template not found for {filename}")

if __name__ == "__main__":
    # Test docxtpl based engine
    test_structure = "document_structure.json"
    generator = DocumentGenerator(
        template_dir="files/marked", 
        output_dir="output", 
        structure_file=test_structure
    )
    
    test_user_data = {
        "company_name": "新世紀虛擬科技股份有限公司",
        "company_short_name": "新世紀",
        "publish_date": "2026/05/20",
        "version": "1.0.0",
        "doc_number": "IS-001",
        "department": "資訊安全處"
    }
    
    print("Testing Batch Engine on entire marked folder...")
    generator.generate_all(test_user_data)
