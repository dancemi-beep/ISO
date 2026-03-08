import os
import json


class IntegrityChecker:
    """Validates document structure completeness and template file existence."""

    def __init__(self, structure_file, template_dir):
        self.template_dir = template_dir

        with open(structure_file, 'r', encoding='utf-8') as f:
            self.structure = json.load(f)

    def check_template_files_exist(self):
        """Check that every file in document_structure.json exists in the template dir."""
        missing = []
        found = []
        for family_key, files in self.structure.items():
            for file_info in files:
                filename = file_info['filename']
                path = os.path.join(self.template_dir, filename)
                if os.path.exists(path):
                    found.append(filename)
                else:
                    missing.append(filename)
        return found, missing

    def check_tier_completeness(self):
        """Ensure each IS-0XX family has at least one Tier 2 (Procedure) document."""
        warnings = []
        for family_key, files in self.structure.items():
            if family_key in ("Other", "IS-001", "IS-018"):
                continue
            tiers = [f.get('tier', '') for f in files]
            has_tier2 = any('Tier 2' in t for t in tiers)
            if not has_tier2:
                warnings.append(
                    f"{family_key}：缺少 Tier 2（程序書）文件，文件體系可能不完整。"
                )
        return warnings

    def check_processable_types(self):
        """Warn about files that are not docx/xlsx which cannot be processed."""
        warnings = []
        for family_key, files in self.structure.items():
            for file_info in files:
                filename = file_info['filename']
                ftype = file_info.get('type', 'word')
                if ftype not in ('word', 'excel'):
                    warnings.append(f"{filename}：類型 '{ftype}' 無法由引擎處理，將跳過。")
                elif ftype == 'word' and not filename.endswith('.docx'):
                    warnings.append(f"{filename}：標記為 word 但副檔名非 .docx，將跳過。")
                elif ftype == 'excel' and not filename.endswith('.xlsx'):
                    warnings.append(f"{filename}：標記為 excel 但副檔名非 .xlsx，將跳過。")
        return warnings

    def run_all_checks(self):
        """Run all integrity checks and return structured results.
        
        Returns:
            dict: {
                "passed": [str],
                "warnings": [str],
                "errors": [str],
                "template_count": int,
                "missing_count": int
            }
        """
        results = {"passed": [], "warnings": [], "errors": []}

        # 1. Template file existence
        found, missing = self.check_template_files_exist()
        results["template_count"] = len(found)
        results["missing_count"] = len(missing)

        if not missing:
            results["passed"].append(f"所有 {len(found)} 份範本檔案皆已就緒。")
        else:
            for m in missing:
                results["errors"].append(f"範本缺失：{m}")

        # 2. Tier completeness
        tier_warnings = self.check_tier_completeness()
        results["warnings"].extend(tier_warnings)
        if not tier_warnings:
            results["passed"].append("所有 IS 文件家族皆包含 Tier 2 程序書。")

        # 3. Processable type check
        type_warnings = self.check_processable_types()
        results["warnings"].extend(type_warnings)
        if not type_warnings:
            results["passed"].append("所有檔案類型皆可由引擎處理。")

        return results


if __name__ == "__main__":
    checker = IntegrityChecker(
        structure_file="document_structure.json",
        template_dir="files/marked"
    )
    results = checker.run_all_checks()

    print("=== 鉤稽檢查結果 ===")
    print(f"\n✅ 通過 ({len(results['passed'])})")
    for p in results['passed']:
        print(f"  • {p}")

    print(f"\n⚠️  警告 ({len(results['warnings'])})")
    for w in results['warnings']:
        print(f"  • {w}")

    print(f"\n❌ 錯誤 ({len(results['errors'])})")
    for e in results['errors']:
        print(f"  • {e}")
