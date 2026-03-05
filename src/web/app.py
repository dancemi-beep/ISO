import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Ensure web reads from the project root correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USER_DATA_PATH = os.path.join(BASE_DIR, "user_data.json")

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
    # Update data with form submission
    req_data = request.form.to_dict()
    data.update(req_data)
    save_user_data(data)
    
    # Redirect to next stage or return success
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
    return render_template("stage4.html", data=data)

@app.route("/api/generate", methods=["POST"])
def generate_all():
    import sys
    # Add engine directory to path temporarily to import DocumentGenerator
    engine_path = os.path.join(BASE_DIR, "src", "engine")
    if engine_path not in sys.path:
        sys.path.append(engine_path)
        
    try:
        from document_generator import DocumentGenerator
        data = load_user_data()
        
        # Setup paths for generator
        template_dir = os.path.join(BASE_DIR, "files", "marked")
        output_dir = os.path.join(BASE_DIR, "output")
        structure_file = os.path.join(BASE_DIR, "document_structure.json")
        
        generator = DocumentGenerator(template_dir, output_dir, structure_file)
        generator.generate_all(data)
        
        # Return success (in a real app we'd zip these up and return a download link)
        return render_template("success.html")
    except Exception as e:
        return f"Generation failed: {str(e)}", 500

if __name__ == "__main__":
    print(f"Starting ISO 27001 Web App. Data will be saved to: {USER_DATA_PATH}")
    app.run(debug=True, port=5000)
