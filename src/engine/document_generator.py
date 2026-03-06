import os
import json
import shutil
from docxtpl import DocxTemplate
import openpyxl


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
        """Generate a single .docx document by replacing variables using docxtpl."""
        try:
            doc = DocxTemplate(template_path)
            context = {var: user_data.get(var, f"[Missing: {var}]") for var in variables}
            doc.render(context)
            doc.save(output_path)
            return True
        except Exception as e:
            print(f"Error processing {template_path}: {e}")
            return False

    def generate_excel(self, template_path, output_path, variables, user_data):
        """Generate a single .xlsx file by copying template and replacing cell values."""
        try:
            shutil.copy2(template_path, output_path)
            wb = openpyxl.load_workbook(output_path)

            # Build replacement map from variables
            replacements = {}
            for var in variables:
                val = user_data.get(var)
                if val is not None:
                    replacements[var] = val

            # Scan all sheets for Jinja-like {{ var }} patterns and replace
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                for row in ws.iter_rows():
                    for cell in row:
                        if cell.value and isinstance(cell.value, str):
                            new_val = cell.value
                            for var, val in replacements.items():
                                new_val = new_val.replace("{{" + var + "}}", str(val))
                                new_val = new_val.replace("{{ " + var + " }}", str(val))
                            if new_val != cell.value:
                                cell.value = new_val

            wb.save(output_path)
            return True
        except Exception as e:
            print(f"Error processing Excel {template_path}: {e}")
            return False

    def generate_all(self, user_data):
        """Iterate through the structure, auto-inject doc_number, and generate all documents.
        
        Returns:
            dict: {"success": [...], "failed": [...], "skipped": [...]}
        """
        result = {"success": [], "failed": [], "skipped": []}

        for family_key, files in self.structure.items():
            for file_info in files:
                filename = file_info['filename']
                variables = file_info.get('variables', [])
                file_type = file_info.get('type', 'word')

                template_path = os.path.join(self.template_dir, filename)
                output_path = os.path.join(self.output_dir, filename)

                if not os.path.exists(template_path):
                    print(f"Warning: Template not found for {filename}")
                    result["skipped"].append(filename)
                    continue

                # Auto-inject doc_number from family key (e.g. "IS-001")
                enriched_data = dict(user_data)
                if 'doc_number' in variables and family_key != "Other":
                    enriched_data.setdefault('doc_number', family_key)

                if file_type == 'word' and filename.endswith('.docx'):
                    ok = self.generate_document(template_path, output_path, variables, enriched_data)
                elif file_type == 'excel' and filename.endswith('.xlsx'):
                    ok = self.generate_excel(template_path, output_path, variables, enriched_data)
                else:
                    print(f"Skipping unsupported type: {filename}")
                    result["skipped"].append(filename)
                    continue

                if ok:
                    print(f"Generated: {filename}")
                    result["success"].append(filename)
                else:
                    result["failed"].append(filename)

        return result


if __name__ == "__main__":
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
        "department": "資訊安全處"
    }

    print("Testing Batch Engine on entire marked folder...")
    result = generator.generate_all(test_user_data)
    print(f"\n--- Summary ---")
    print(f"Success: {len(result['success'])}")
    print(f"Failed:  {len(result['failed'])}")
    print(f"Skipped: {len(result['skipped'])}")
