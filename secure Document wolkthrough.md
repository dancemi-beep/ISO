# 文件安全防護 (Know-how 保護) 實作成果

我們已成功實作並驗證了文件範本的加密保護機制。現在，系統中的原始 Word 與 Excel 範本均以 AES-256 加密存儲，防止被直接取用。

## 實作內容

### 1. 安全引擎 (Security Engine)
- **檔案**: [security.py](file:///Users/imitate/Desktop/iso_dev/src/engine/security.py)
- **功能**: 使用 AES-256 (Fernet) 進行數據加密與解密。
- **保護**: 範本檔案在磁碟上始終保持加密狀態，僅在生成文件時於記憶體中即時解密。

### 2. 範本加密工具
- **檔案**: [encrypt_templates.py](file:///Users/imitate/Desktop/iso_dev/tools/encrypt_templates.py)
- **成果**: 已將 `files/marked/` 下所有 60 個範本檔案加密為 `.enc` 格式，並移除了原始明文。

### 3. 生成引擎升級
- **檔案**: [document_generator.py](file:///Users/imitate/Desktop/iso_dev/src/engine/document_generator.py)
- **成果**: 自動偵測 `.enc` 加密檔，並支援從記憶體載入解密後的範本進行渲染。

---

## 驗證結果

### 範本保護測試
- **原始路徑**: `files/marked/IS-001 資訊安全政策.docx` (已不存在)
- **現有路徑**: `files/marked/IS-001 資訊安全政策.docx.enc` (無法直接開啟，受保護)

### 生成功能驗證
執行 `verify_security.py` 進行端到端測試：
- **操作**: 從加密範本 `IS-001...docx.enc` 生成 `TST-001...docx`。
- **結果**: **成功**。生成的文件為標準 Word 格式，且內容正確替換。

---

## 後續建議
- **密鑰管理**: 目前使用固定的內置密鑰。未來可升級為配合客戶電腦硬體資訊 (UUID/MAC) 生成動態密鑰，實現真正的「單機授權」。
- **發布流程**: 在打包 ZIP 給客戶前，務必執行 `tools/encrypt_templates.py`。
