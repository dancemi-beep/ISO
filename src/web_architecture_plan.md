# Phase 3: System Front-End (Web UI) Architecture Plan

此階段將建立使用者操作介面，以引導式的問卷形式收集資訊，並串接 Phase 2 完成的生成引擎。

## 1. 架構選型 (Technology Stack)
* **後端框架**: `Flask` (輕量、適合快速構建 POC 與單機版應用)
* **前端技術**: `HTML5`, `CSS3` (建議導入 TailwindCSS 或是 Bootstrap 以快速建立美觀、RWD 的表單介面), Vanilla `JavaScript` (處理不同階段的表單動態切換與前端基本驗證)
* **資料儲存**: `TinyDB` 或單純的 `.json` 檔案 (配合系統單機執行的特性，不使用重量級關聯資料庫)

## 2. 專案目錄結構設計 (Directory Structure)
```
iso_dev/
├── files/                  # 原始 ISO 範本
├── files/marked/           # [已完成] 標籤化範本
├── output/                 # 最終生成的客製化文件存放區
├── src/
│   ├── engine/             # [已完成] Phase 2 生成引擎
│   │   ├── document_generator.py
│   │   └── batch_tagger.py
│   └── web/                # [Phase 3 新增] Web 應用程式層
│       ├── app.py          # Flask 啟動檔與主要 Routing
│       ├── static/         # CSS, JS, Images
│       └── templates/      # HTML 視圖
│           ├── base.html   # 共用版型
│           ├── stage1.html # 階段一：啟動與範圍 (公司資料)
│           ├── stage2.html # 階段二：資產盤點與風險評鑑
│           ├── stage3.html # 階段三：管理程序與自訂規定
│           └── stage4.html # 階段四：產出與下載
├── document_structure.json # [已完成] 文件變數對應表
└── user_data.json          # [Phase 3 新增] 儲存使用者的問卷作答
```

## 3. 四階段路由與引導邏輯 (Routing Logic)

* `GET /`: 首頁，專案介紹與「開始導入 ISO 27001」按鈕。
* `GET /stage/1`: 渲染階段一問卷表單 (收集 `company_name`, `publish_date` 等 Phase 2 我們盤點的基礎共通變數)。
* `POST /api/save/1`: 儲存階段一資料至 `user_data.json`，並回傳 next_stage url。
* `GET /stage/2`: 渲染階段二問卷表單 (收集系統資產清單、預設的威脅/弱點/衝擊評分，以及自訂的 `acceptable_risk_level`)。
* `POST /api/save/2`: ...
* `GET /stage/4`: 總結頁面，顯示已收集的所有變數。提供「一鍵產生文件」按鈕。
* `POST /api/generate`: 呼叫 `src/engine/document_generator.py`，傳入完整的 `user_data.json` 進行批次產生。完成後提供 Zip 下載。

## 4. 下一步執行項目 (Next Steps for Execution)
1. 在專案中建立 `src/web/` 的基礎資料夾結構。
2. 撰寫基礎的 `app.py` 並啟動 Flask 伺服器，確保網頁能正常路由。
3. 建立 `base.html` 基礎框架與套用簡單美觀的 CSS (Tailwind)。
