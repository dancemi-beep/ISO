import os
import re
import docx

def replace_text_in_doc_runs_safe(doc, old_text, new_text):
    """
    Safely replace text without merging runs if possible.
    Since docxtpl needs the exact {{ variable_name }} syntax inside a single run,
    or at least unbroken, we try to clear out the paragraph.text entirely or replace run by run.
    For this pre-processing step, since we want to enforce {{ var }} into a single run for docxtpl to parse later,
    replacing para.text wholesale is actually safer in generating valid Jinja templates, 
    even if we lose some granular inline styling during preparation.
    """
    for para in doc.paragraphs:
        if old_text in para.text:
            # Simple fallback for preparation:
            para.text = para.text.replace(old_text, new_text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if old_text in para.text:
                        para.text = para.text.replace(old_text, new_text)

    for section in doc.sections:
        for para in section.header.paragraphs:
            if old_text in para.text:
                para.text = para.text.replace(old_text, new_text)
        for para in section.footer.paragraphs:
            if old_text in para.text:
                para.text = para.text.replace(old_text, new_text)

def batch_mark_templates(directory):
    # Mapping of common hardcoded Taiwanese strings found in boilerplate to Jinja variables
    # Add more to this dict if you find other consistent hardcoded default values
    replacements = {
        "XXXX股份有限公司": "{{company_name}}",
        "公司系統代碼": "{{company_short_name}}",  # Placeholder guess
        "年/月/日": "{{publish_date}}",
        "YYYY/MM/DD": "{{publish_date}}"
    }
    
    # We will output prepared templates into a new folder so we don't destructively overwrite inputs
    output_dir = os.path.join(directory, "marked")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for f in os.listdir(directory):
        if not f.endswith('.docx') or f.startswith('~'):
            continue
            
        filepath = os.path.join(directory, f)
        outpath = os.path.join(output_dir, f)
        
        try:
            doc = docx.Document(filepath)
            changed = False
            for old_str, jinja_var in replacements.items():
                # We do a quick check to save doc processing time
                replace_text_in_doc_runs_safe(doc, old_str, jinja_var)
                changed = True  # Assuming it replaced, we'll save it anyway for simplicity
            
            doc.save(outpath)
            print(f"Processed template: {f}")
        except Exception as e:
            print(f"Error marking {f}: {e}")

if __name__ == "__main__":
    target_dir = "files"
    print(f"Starting batch marking in {target_dir}...")
    batch_mark_templates(target_dir)
    print("Done. Check files/marked/")
