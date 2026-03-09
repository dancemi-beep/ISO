import os
import sys
import json
import zipfile
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file

# Ensure web reads from the project root correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USER_DATA_PATH = os.path.join(BASE_DIR, "user_data.json")

# Add engine directory to path
ENGINE_PATH = os.path.join(BASE_DIR, "src", "engine")
if ENGINE_PATH not in sys.path:
    sys.path.insert(0, ENGINE_PATH)

# Load questionnaire config
QUESTIONNAIRE_CONFIG_PATH = os.path.join(BASE_DIR, "questionnaire_config.json")
with open(QUESTIONNAIRE_CONFIG_PATH, "r", encoding="utf-8") as f:
    QUESTIONNAIRE_CONFIG = json.load(f)

app = Flask(__name__)


def get_stage_fields(stage_num):
    """Get questionnaire fields and sections for a given stage."""
    key = f"stage{stage_num}"
    config = QUESTIONNAIRE_CONFIG.get(key, {})
    sections = config.get("sections", [])
    # Flatten fields from sections for backward compat
    fields = []
    for section in sections:
        fields.extend(section.get("fields", []))
    if not fields:
        fields = config.get("fields", [])
    return fields, sections, config.get("title", "")


def compute_derived_variables(data):
    """Compute derived variables from user input."""
    # publish_date_short: extract year suffix (e.g. '2026/05/20' -> '26')
    pd = data.get('publish_date', '')
    if '/' in pd and len(pd) >= 4:
        data['publish_date_short'] = pd[2:4]  # e.g. '20' from '2026'
    
    # dept_name: use committee dept fields
    for key in ['security_committee_dept1', 'security_committee_dept2']:
        val = data.get(key, '')
        if val and 'dept_name' not in data:
            data['dept_name'] = val
    
    return data


def load_user_data():
    if os.path.exists(USER_DATA_PATH):
        try:
            with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_user_data(data):
    with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ─── Routes ───────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stage/1", methods=["GET"])
def stage1():
    data = load_user_data()
    fields, sections, title = get_stage_fields(1)
    return render_template("stage1.html", data=data, fields=fields, sections=sections, stage_title=title)


@app.route("/api/save/1", methods=["POST"])
def save_stage1():
    data = load_user_data()
    req_data = request.form.to_dict()
    data.update(req_data)
    save_user_data(data)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success", "next_url": url_for("stage2")})
    return redirect(url_for("stage2"))


@app.route("/stage/2", methods=["GET"])
def stage2():
    data = load_user_data()
    fields, sections, title = get_stage_fields(2)
    return render_template("stage2.html", data=data, fields=fields, sections=sections, stage_title=title)


@app.route("/api/save/2", methods=["POST"])
def save_stage2():
    data = load_user_data()
    req_data = request.form.to_dict()
    data.update(req_data)
    save_user_data(data)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success", "next_url": url_for("stage3")})
    return redirect(url_for("stage3"))


@app.route("/stage/3", methods=["GET"])
def stage3():
    data = load_user_data()
    fields, sections, title = get_stage_fields(3)
    return render_template("stage3.html", data=data, fields=fields, sections=sections, stage_title=title)


@app.route("/api/save/3", methods=["POST"])
def save_stage3():
    data = load_user_data()
    req_data = request.form.to_dict()
    data.update(req_data)
    save_user_data(data)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success", "next_url": url_for("stage4")})
    return redirect(url_for("stage4"))


@app.route("/stage/4", methods=["GET"])
def stage4():
    data = load_user_data()

    # Run integrity checks
    from integrity_checker import IntegrityChecker
    template_dir = os.path.join(BASE_DIR, "files", "marked")
    structure_file = os.path.join(BASE_DIR, "document_structure.json")
    checker = IntegrityChecker(structure_file, template_dir)
    check_results = checker.run_all_checks()

    return render_template("stage4.html", data=data, checks=check_results)


@app.route("/api/generate", methods=["POST"])
def generate_all():
    try:
        from document_generator import DocumentGenerator
        from readme_generator import ReadmeGenerator

        data = load_user_data()
        data = compute_derived_variables(data)

        template_dir = os.path.join(BASE_DIR, "files", "marked")
        output_dir = os.path.join(BASE_DIR, "output")
        structure_file = os.path.join(BASE_DIR, "document_structure.json")

        # Clear existing output files to prevent old files entering the zip
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            for f in os.listdir(output_dir):
                fp = os.path.join(output_dir, f)
                if os.path.isfile(fp):
                    os.remove(fp)

        # Generate all documents
        generator = DocumentGenerator(template_dir, output_dir, structure_file)
        result = generator.generate_all(data)

        # Generate readme
        readme_gen = ReadmeGenerator(structure_file)
        readme_gen.generate(data, output_dir, generated_files=result["success"])

        # Generate Questionnaire Report
        from questionnaire_report import QuestionnaireReportGenerator
        config_path = os.path.join(BASE_DIR, "questionnaire_config.json")
        q_gen = QuestionnaireReportGenerator(config_path)
        q_report_path = os.path.join(output_dir, "問卷填答總表.docx")
        q_gen.generate(data, q_report_path)

        doc_prefix = str(data.get("doc_prefix", "IS")).strip()
        if not doc_prefix:
            doc_prefix = "IS"

        def apply_prefix(text):
            if not text: return text
            if text.startswith("IS"):
                return text.replace("IS", doc_prefix, 1)
            return text

        # Create ZIP package with structured folders
        zip_path = os.path.join(output_dir, "ISMS文件包.zip")
        
        file_to_arcname = {}
        for original_fkey, flist in generator.structure.items():
            fkey = apply_prefix(original_fkey)
            if original_fkey == "Other":
                folder_name = "其他文件"
            else:
                main_doc = next((f['filename'] for f in flist if 'Tier 1' in f.get('tier','') or 'Tier 2' in f.get('tier','')), None)
                if main_doc:
                    main_doc = apply_prefix(main_doc)
                folder_name = (os.path.splitext(main_doc)[0] if main_doc else fkey).replace(" ", "-")
                
            for f in flist:
                tier = f.get('tier', '')
                fname = apply_prefix(f['filename'])
                if original_fkey == "Other":
                    file_to_arcname[fname] = f"{folder_name}/{fname}"
                elif 'Tier 1' in tier or 'Tier 2' in tier:
                    file_to_arcname[fname] = f"{folder_name}/{fname}"
                else:
                    file_to_arcname[fname] = f"{folder_name}/表單/{fname}"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Create empty directory structures
            for original_fkey, flist in generator.structure.items():
                if original_fkey == "Other": continue
                fkey = apply_prefix(original_fkey)
                main_doc = next((f['filename'] for f in flist if 'Tier 1' in f.get('tier','') or 'Tier 2' in f.get('tier','')), None)
                if main_doc:
                    main_doc = apply_prefix(main_doc)
                folder_name = (os.path.splitext(main_doc)[0] if main_doc else fkey).replace(" ", "-")
                zf.writestr(f"{folder_name}/紀錄/", b'')
                zf.writestr(f"{folder_name}/表單/", b'')

            for fname in os.listdir(output_dir):
                fpath = os.path.join(output_dir, fname)
                if fname.endswith('.zip') or fname.startswith('~') or fname.startswith('.'):
                    continue
                if os.path.isfile(fpath):
                    if fname == "問卷填答總表.docx":
                        zf.write(fpath, fname) # Root level
                    else:
                        arcname = file_to_arcname.get(fname, fname)
                        zf.write(fpath, arcname)

            # Auto-inject Example Files
            examples_dir = os.path.join(BASE_DIR, "examples")
            if os.path.exists(examples_dir):
                for fname in os.listdir(examples_dir):
                    if fname.startswith('.') or fname.startswith('~'):
                        continue
                    fpath = os.path.join(examples_dir, fname)
                    if os.path.isfile(fpath):
                        # Try to match the prefix e.g., "IS-001-01範例.pdf" -> "IS-001-01"
                        import re
                        match = re.search(r'(IS-\d{3}(?:-\d{2})?)', fname)
                        if match:
                            prefix = apply_prefix(match.group(1))
                            new_fname = fname.replace("IS", doc_prefix, 1) if fname.startswith("IS") else fname

                            # Strip out inconsistent example naming artifacts and replace with a clean format
                            # Match things like "範例", "(範例)", "（範例）", "_範例", " (範例) "
                            new_fname = re.sub(r'[\(\（\_ ]*範例[\)\） ]*', '', new_fname)
                            # Put a clean "(範本)" or just "_範例" depending on format - let's standardise to "-(範例)"
                            name_part, ext_part = os.path.splitext(new_fname)
                            new_fname = f"{name_part}-範例{ext_part}"

                            # Find which folder it belongs to
                            target_arcname = f"其他文件/範本_{new_fname}"
                            for k, fn in file_to_arcname.items():
                                if k.startswith(prefix):
                                    base_dir = os.path.dirname(fn)
                                    target_arcname = f"{base_dir}/{new_fname}"
                                    break
                            zf.write(fpath, target_arcname)
                        else:
                            # If no prefix match, put it in root
                            zf.write(fpath, f"參考範例_{fname}")

        return render_template("success.html", result=result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Generation failed: {str(e)}", 500


@app.route("/api/download")
def download_zip():
    zip_path = os.path.join(BASE_DIR, "output", "ISMS文件包.zip")
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name="ISMS文件包.zip")
    return "ZIP file not found. Please generate documents first.", 404


if __name__ == "__main__":
    print(f"Starting ISO 27001 Web App. Data will be saved to: {USER_DATA_PATH}")
    app.run(debug=True, port=5001)
