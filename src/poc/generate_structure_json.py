import os
import json
import re

files_dir = 'files'
output_json = 'document_structure.json'

def guess_tier_and_type(filename):
    if filename.endswith('.xlsx'):
        doc_type = 'excel'
    elif filename.endswith('.pdf'):
        doc_type = 'pdf'
    else:
        doc_type = 'word'
        
    tier = "Unknown"
    # Basic heuristic for ISO tiers (1: Manual/Policy, 2: Procedure, 3: Work Instruction, 4: Record/Form)
    if '政策' in filename or '聲明書' in filename:
        tier = "Tier 1 - Policy"
    elif '程序' in filename:
        tier = "Tier 2 - Procedure"
    elif '表' in filename or '單' in filename or '紀錄' in filename or '紀錄' in filename or '報告' in filename or '計畫' in filename or '切結書' in filename or '分析' in filename:
        tier = "Tier 4 - Record/Form"
    else:
        tier = "Tier 3 - Guideline/Instruction" # Fallback guess
        
    return tier, doc_type

def main():
    structure = {}
    
    if not os.path.exists(files_dir):
        print(f"Directory {files_dir} not found.")
        return

    for f in os.listdir(files_dir):
        if f.startswith('.') or f.startswith('~'):
            continue
            
        # Extract prefix like IS-001 or IS003
        match = re.match(r'^(IS-?\d{3})', f)
        if match:
            family = match.group(1).replace('IS0', 'IS-0') # Normalize IS003 to IS-003
        else:
            family = 'Other'
            
        if family not in structure:
            structure[family] = []
            
        tier, doc_type = guess_tier_and_type(f)
        
        structure[family].append({
            "filename": f,
            "tier": tier,
            "type": doc_type,
            "variables": [] # To be filled later
        })
        
    # Sort structure by family
    sorted_structure = {k: sorted(v, key=lambda x: x['filename']) for k, v in sorted(structure.items())}
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(sorted_structure, f, ensure_ascii=False, indent=4)
        
    print(f"Structure saved to {output_json}")

if __name__ == '__main__':
    main()
