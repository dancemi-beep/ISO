import json

input_json = 'document_structure.json'
output_json = 'document_structure.json'

common_variables = [
    "company_name",
    "company_short_name",
    "publish_date",
    "version",
    "doc_number",
    "department"
]

def main():
    try:
        with open(input_json, 'r', encoding='utf-8') as f:
            structure = json.load(f)
    except FileNotFoundError:
        print(f"File {input_json} not found.")
        return

    for family, files in structure.items():
        for file_info in files:
            # Add common variables to the existing 'variables' list, avoiding duplicates
            existing_vars = set(file_info.get("variables", []))
            for v in common_variables:
                if v not in existing_vars:
                    file_info.setdefault("variables", []).append(v)
            
            # Add specific variables based on family
            if family == "IS-002" and file_info.get("tier") == "Tier 4 - Record/Form" and "全景評鑑表" in file_info.get("filename"):
                if "iso_scope" not in file_info["variables"]:
                    file_info["variables"].append("iso_scope")
            elif family == "IS-004" and file_info.get("tier") == "Tier 4 - Record/Form" and "風險評鑑表" in file_info.get("filename"):
                if "acceptable_risk_level" not in file_info["variables"]:
                    file_info["variables"].append("acceptable_risk_level")
            elif family == "IS-018" and file_info.get("tier") == "Tier 1 - Policy" and "適用性聲明書" in file_info.get("filename"):
                if "soa_version" not in file_info["variables"]:
                     file_info["variables"].append("soa_version")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully updated {output_json} with variables.")

if __name__ == '__main__':
    main()
