# ISO 27001 ISMS 導入文件生成系統

一套協助企業自動產出 ISO 27001 資訊安全管理系統 (ISMS) 全套文件的本機工具。

## 功能特色

- **四階段引導問卷**：從公司基本資料 → 風險評鑑 → 管理程序 → 體系檢查，循序漸進完成所有設定
- **59 份文件自動生成**：涵蓋一至四階層（政策、程序書、作業指導書、表單紀錄），支援 `.docx` 與 `.xlsx`
- **體系鉤稽檢查**：自動檢測範本完整性與文件階層是否齊全
- **導入指引手冊**：自動產出簽核流程建議與維運提醒
- **ZIP 一鍵下載**：全部文件打包壓縮，方便匯出
- **單機執行**：所有資料僅存於本機，符合資安要求

## 系統需求

- Python 3.10 以上
- macOS / Linux / Windows (需使用 Git Bash 或 WSL)

## 快速啟動

```bash
# 1. 賦予啟動腳本執行權限（首次）
chmod +x start.sh

# 2. 一鍵啟動
./start.sh
```

啟動後開啟瀏覽器前往 **http://localhost:5001** 即可使用。

## 手動啟動

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝套件
pip install -r requirements.txt

# 啟動伺服器
python src/web/app.py
```

## 專案結構

```
iso_dev/
├── start.sh                    ← 一鍵啟動腳本
├── requirements.txt            ← Python 依賴
├── document_structure.json     ← 四階層文件變數定義
│
├── files/
│   └── marked/                 ← ★ 已標籤化的範本（引擎讀取來源）
│
├── src/
│   ├── engine/
│   │   ├── document_generator.py   ← 核心生成引擎 (docxtpl + openpyxl)
│   │   ├── batch_tagger.py         ← 批次標籤化工具
│   │   ├── integrity_checker.py    ← 體系鉤稽檢查
│   │   └── readme_generator.py     ← 導入指引手冊生成
│   │
│   ├── web/
│   │   ├── app.py                  ← Flask 後端
│   │   └── templates/              ← 前端頁面 (Jinja2)
│   │
│   └── tests/
│       └── test_e2e.py             ← 端到端測試
│
├── output/                     ← 生成的文件輸出目錄
├── current.md                  ← 開發進度追蹤
├── plan.md                     ← 開發計畫
├── version.md                  ← 版本紀錄
└── sys_spec.md                 ← 系統規格書
```

## 使用流程

1. 啟動系統（`./start.sh`）
2. 瀏覽器開啟 http://localhost:5001
3. **階段一**：填寫公司基本資料、驗證範圍
4. **階段二**：設定資產盤點與風險閾值
5. **階段三**：確認管理程序與規定
6. **階段四**：檢視鉤稽結果 → 一鍵生成 → 下載 ZIP
7. 解壓 ZIP，參閱「導入指引手冊.docx」進行後續簽核

## 如何新增或修改範本

### 修改現有範本

1. 開啟 `files/marked/` 中的 `.docx` 檔案
2. 使用 `{{ 變數名 }}` 語法標記需要動態替換的位置，例如：
   - `{{ company_name }}` → 公司全名
   - `{{ company_short_name }}` → 公司簡稱
   - `{{ publish_date }}` → 發布日期
   - `{{ version }}` → 版本號
   - `{{ department }}` → 權責部門
3. 儲存後直接覆蓋原檔即可

### 新增範本

1. 建立新的 `.docx` 或 `.xlsx` 檔案，放入 `files/marked/`
2. 在檔案中使用 `{{ 變數名 }}` 標記動態欄位
3. 編輯 `document_structure.json`，加入新檔案的定義：

```json
{
    "IS-NEW": [
        {
            "filename": "IS-NEW-新模組.docx",
            "tier": "Tier 2 - Procedure",
            "type": "word",
            "variables": ["company_name", "publish_date", "version"]
        }
    ]
}
```

4. 重新啟動系統即可

### 支援的變數類型

| 變數 | 說明 | 來源階段 |
|---|---|---|
| `company_name` | 公司全名 | 階段一 |
| `company_short_name` | 公司簡稱 | 階段一 |
| `publish_date` | 文件發布日期 | 階段一 |
| `version` | 文件版本號 | 階段一 |
| `department` | 權責部門 | 階段一 |
| `doc_number` | 文件編碼（自動依 family key 注入） | 自動 |
| `acceptable_risk_level` | 可接受風險值 | 階段二 |

## 執行測試

```bash
source venv/bin/activate
python -m pytest src/tests/test_e2e.py -v
```

## 技術棧

| 項目 | 技術 |
|---|---|
| 後端框架 | Flask 3.x |
| 文件引擎 | docxtpl (Jinja2) + python-docx |
| Excel 處理 | openpyxl |
| 前端 | HTML + TailwindCSS + Font Awesome |
| 部署方式 | 單機 Localhost (資安考量) |
