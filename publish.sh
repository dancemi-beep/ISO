#!/bin/bash
# ISO 27001 客端封裝腳本 (Publish Script)
# 功能：自動加密範本、清理開發工具、打包成 ZIP

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$PROJECT_DIR/dist_package"
ZIP_NAME="ISO27001_Generator_v1.zip"

echo "=========================================="
echo "  開始生成客戶發布包..."
echo "=========================================="

# 1. 建立乾淨的發布目錄
echo "📂 整理髮布目錄..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 2. 複製必要檔案 (最小化發布)
mkdir -p "$DIST_DIR/files"
cp -R "$PROJECT_DIR/files/marked" "$DIST_DIR/files/"
cp -R "$PROJECT_DIR/examples" "$DIST_DIR/"
cp -R "$PROJECT_DIR/src" "$DIST_DIR/"
cp "$PROJECT_DIR/start.sh" "$DIST_DIR/"
cp "$PROJECT_DIR/requirements.txt" "$DIST_DIR/"
cp "$PROJECT_DIR/document_structure.json" "$DIST_DIR/"
cp "$PROJECT_DIR/questionnaire_config.json" "$DIST_DIR/"

# 3. 處理文件轉 PDF
echo "📄 正在將說明文件轉換為 PDF..."
PYTHONPATH="$PROJECT_DIR/src/engine" "$PROJECT_DIR/venv/bin/python3" "$PROJECT_DIR/tools/md_to_pdf.py" \
    "$PROJECT_DIR/安裝與使用手冊.md" "$DIST_DIR/安裝與使用手冊.pdf"

# 4. 在發布目錄中執行加密 (保護所有 Know-how)
if [ -f "$PROJECT_DIR/tools/encrypt_templates.py" ]; then
    echo "🔐 正在加密發布包中的範本與設定檔..."
    PYTHONPATH="$PROJECT_DIR/src/engine" "$PROJECT_DIR/venv/bin/python3" "$PROJECT_DIR/tools/encrypt_templates.py" \
        --mode encrypt --yes \
        --dirs "$DIST_DIR/files/marked" "$DIST_DIR/examples" \
               "$DIST_DIR/document_structure.json" "$DIST_DIR/questionnaire_config.json"
else
    echo "⚠️ 找不到加密工具！"
fi

# 5. 源碼保護：編譯為 Bytecode 並移除原始碼
echo "🔐 正在編譯 Python 原始碼為 Bytecode (.pyc)..."
# 使用系統預設 python3 進行編譯，以確保與進入點使用的版本一致
python3 -m compileall -b "$DIST_DIR/src"
find "$DIST_DIR/src" -name "*.py" -delete

# 6. 最終清理 (絕對不允許明文開發檔案外流)
echo "🧹 徹底清理開發檔案與原始 MD..."
rm -rf "$DIST_DIR/src/engine/tests"
rm -rf "$DIST_DIR/src/poc"
rm -rf "$DIST_DIR/tools"
rm -f "$DIST_DIR/verify_security.py"
rm -f "$DIST_DIR/src/web_architecture_plan.md"
rm -f "$DIST_DIR/README.md"
find "$DIST_DIR" -name "__pycache__" -exec rm -rf {} +
find "$DIST_DIR" -name ".DS_Store" -delete

# 7. 修改進入點
sed -i '' 's/python3 "$SCRIPT_DIR\/src\/web\/app.py"/python3 "$SCRIPT_DIR\/src\/web\/app.pyc"/' "$DIST_DIR/start.sh"
# 如果舊版是 python，也要處理
sed -i '' 's/python "$SCRIPT_DIR\/src\/web\/app.py"/python3 "$SCRIPT_DIR\/src\/web\/app.pyc"/' "$DIST_DIR/start.sh"

# 8. 打包成 ZIP
echo "📦 正在打包發布檔 ($ZIP_NAME)..."
cd "$DIST_DIR"
zip -r "../$ZIP_NAME" . > /dev/null

echo "=========================================="
echo "✅ 發布包生成成功！"
echo "📎 檔案位置：$PROJECT_DIR/$ZIP_NAME"
echo "=========================================="
