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

app = Flask(__name__)


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
    return render_template("stage1.html", data=data)


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
    return render_template("stage2.html", data=data)


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
    return render_template("stage3.html", data=data)


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

        template_dir = os.path.join(BASE_DIR, "files", "marked")
        output_dir = os.path.join(BASE_DIR, "output")
        structure_file = os.path.join(BASE_DIR, "document_structure.json")

        # Generate all documents
        generator = DocumentGenerator(template_dir, output_dir, structure_file)
        result = generator.generate_all(data)

        # Generate readme
        readme_gen = ReadmeGenerator(structure_file)
        readme_gen.generate(data, output_dir, generated_files=result["success"])

        # Create ZIP package
        zip_path = os.path.join(output_dir, "ISMS文件包.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fname in os.listdir(output_dir):
                fpath = os.path.join(output_dir, fname)
                # Don't zip the zip itself, or temp files
                if fname.endswith('.zip') or fname.startswith('~') or fname.startswith('.'):
                    continue
                if os.path.isfile(fpath):
                    zf.write(fpath, fname)

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
