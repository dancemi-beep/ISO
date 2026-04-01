#!/bin/bash
# ISO 27001 ISMS 文件生成系統 — 一鍵啟動腳本
# 使用方式：在終端機執行 ./start.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "=========================================="
echo "  ISO 27001 ISMS 文件生成系統"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 python3，請先安裝 Python 3.10 以上版本。"
    exit 1
fi

# Create venv if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 首次啟動：建立虛擬環境..."
    python3 -m venv "$VENV_DIR"
    echo "📦 安裝必要套件..."
    "$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
    echo "✅ 環境建立完成！"
    echo ""
fi

# Activate
source "$VENV_DIR/bin/activate"

# Ensure dependencies are installed
pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null

echo "🚀 啟動伺服器中..."
echo "📎 開啟瀏覽器前往 → http://localhost:5001"
echo "📎 按 Ctrl+C 可停止伺服器"
echo ""

python "$SCRIPT_DIR/src/web/app.py"
