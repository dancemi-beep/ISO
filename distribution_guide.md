# 生成封裝檔步驟 (Know-how 保護版)

為了確保交付給客戶的 Know-how (範本文件) 受到保護，請按照以下步驟操作：

## 1. 執行自動化發布腳本 (推薦)
我們提供了一個 [publish.sh](file:///Users/imitate/Desktop/iso_dev/publish.sh) 腳本，會自動執行加密、清理與打包。
```bash
# 在專案根目錄執行
chmod +x publish.sh
./publish.sh
```
此腳本會產生 `ISO27001_Generator_v1.zip`。

## 2. 手動操作步驟 (若腳本不可用)
若需手動操作，請嚴格遵守以下順序：

### A. 加密範本 (核心保護)
執行加密工具，將 `files/marked` 中的 `.docx` / `.xlsx` 轉換為不可直接讀取的 `.enc` 檔案。
```bash
PYTHONPATH=src/engine python3 tools/encrypt_templates.py
# 輸入 'y' 確認執行
```

### B. 清理專案環境
刪除客戶不需要、或涉及開發細節的檔案：
- **`venv/`**: 客戶會執行 `start.sh` 自行建立。
- **`.git/`**: 移除版本控制紀錄。
- **`tools/`**: **重要！** 不要把加密工具交付給客戶。
- **`src/engine/tests/`**: 移除測試程式碼。
- **`verify_security.py`**: 移除驗證腳本。
- **`__pycache__` / `.DS_Store`**: 清理快取與 Mac 系統隱藏檔。

### C. 打包 ZIP
將排除上述檔案後的目錄內容，壓縮為 ZIP 檔案交付給客戶。

---

> [!IMPORTANT]
> **發布前檢查**：打開 ZIP 檔檢查 `files/marked/` 目錄，確認裡面「沒有」任何可以直接打開的 `.docx` 或 `.xlsx` 檔案，全部都應該是 `.enc` 結尾。
