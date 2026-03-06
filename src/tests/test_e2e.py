"""
End-to-End test for ISO 27001 Document Generation System.
Uses Flask test client to simulate the full 4-stage workflow.
"""
import os
import sys
import json
import zipfile
import pytest

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(BASE_DIR, "src", "engine")
WEB_DIR = os.path.join(BASE_DIR, "src", "web")

if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)
if WEB_DIR not in sys.path:
    sys.path.insert(0, WEB_DIR)


@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_data():
    return {
        "company_name": "E2E測試科技股份有限公司",
        "company_short_name": "E2E測試",
        "publish_date": "2026/03/06",
        "version": "1.0.0",
        "department": "資訊安全處",
        "acceptable_risk_level": "25",
    }


class TestE2EWorkflow:
    """Test the complete 4-stage workflow."""

    def test_index_loads(self, client):
        rv = client.get("/")
        assert rv.status_code == 200

    def test_stage1_loads(self, client):
        rv = client.get("/stage/1")
        assert rv.status_code == 200

    def test_save_stage1(self, client, test_data):
        rv = client.post("/api/save/1", data=test_data, follow_redirects=True)
        assert rv.status_code == 200

    def test_save_stage2(self, client, test_data):
        rv = client.post("/api/save/2", data=test_data, follow_redirects=True)
        assert rv.status_code == 200

    def test_save_stage3(self, client, test_data):
        rv = client.post("/api/save/3", data=test_data, follow_redirects=True)
        assert rv.status_code == 200

    def test_stage4_shows_integrity_checks(self, client):
        rv = client.get("/stage/4")
        assert rv.status_code == 200
        # Should contain integrity check results
        html = rv.data.decode("utf-8")
        assert "鉤稽檢查結果" in html

    def test_full_generate(self, client, test_data):
        """Full E2E: save data through stages, trigger generation, verify output."""
        # Save user data
        client.post("/api/save/1", data=test_data)
        client.post("/api/save/2", data=test_data)
        client.post("/api/save/3", data=test_data)

        # Trigger generation
        rv = client.post("/api/generate")
        assert rv.status_code == 200
        html = rv.data.decode("utf-8")
        assert "恭喜" in html or "成功" in html

        # Verify output directory has files
        output_dir = os.path.join(BASE_DIR, "output")
        output_files = [f for f in os.listdir(output_dir) if not f.startswith('.') and not f.startswith('~')]
        assert len(output_files) >= 50, f"Expected >= 50 output files, got {len(output_files)}"

        # Verify ZIP exists
        zip_path = os.path.join(output_dir, "ISMS文件包.zip")
        assert os.path.exists(zip_path), "ZIP file should exist"

        # Verify ZIP can be opened and has content
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zip_entries = zf.namelist()
            assert len(zip_entries) >= 50, f"ZIP should have >= 50 entries, got {len(zip_entries)}"
            # Verify readme is included
            assert "導入指引手冊.docx" in zip_entries, "ZIP should contain 導入指引手冊.docx"

    def test_download_zip(self, client, test_data):
        """Ensure /api/download returns the ZIP file after generation."""
        # First generate
        client.post("/api/save/1", data=test_data)
        client.post("/api/generate")

        rv = client.get("/api/download")
        assert rv.status_code == 200
        assert "zip" in rv.content_type or rv.headers.get("Content-Disposition", "")


class TestIntegrityChecker:
    """Test the integrity checker independently."""

    def test_run_all_checks(self):
        from integrity_checker import IntegrityChecker
        structure_file = os.path.join(BASE_DIR, "document_structure.json")
        template_dir = os.path.join(BASE_DIR, "files", "marked")
        checker = IntegrityChecker(structure_file, template_dir)
        results = checker.run_all_checks()

        assert "passed" in results
        assert "warnings" in results
        assert "errors" in results
        assert isinstance(results["template_count"], int)


class TestDocumentGenerator:
    """Test the document generator independently."""

    def test_generate_all_returns_summary(self, test_data):
        from document_generator import DocumentGenerator
        structure_file = os.path.join(BASE_DIR, "document_structure.json")
        template_dir = os.path.join(BASE_DIR, "files", "marked")
        output_dir = os.path.join(BASE_DIR, "output")

        gen = DocumentGenerator(template_dir, output_dir, structure_file)
        result = gen.generate_all(test_data)

        assert "success" in result
        assert "failed" in result
        assert "skipped" in result
        assert len(result["success"]) > 0, "Should have generated at least some files"


class TestReadmeGenerator:
    """Test the readme generator independently."""

    def test_generate_readme(self, test_data):
        from readme_generator import ReadmeGenerator
        structure_file = os.path.join(BASE_DIR, "document_structure.json")
        output_dir = os.path.join(BASE_DIR, "output")

        gen = ReadmeGenerator(structure_file)
        path = gen.generate(test_data, output_dir)
        assert os.path.exists(path)
        assert path.endswith("導入指引手冊.docx")
