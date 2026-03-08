# 版本更新紀錄 (Version History)

## v0.7.0 - 2026-03-08
* **狀態**: Phase 7 完成 — 測試回饋修復與新增報告/範例功能
* **更新內容**:
  * [修復] `IS-001-03` 密碼到期條文與問卷同步。
  * [修復] `IS-004-03` 風險值條文自動帶入。
  * [修復] `IS-003` 目錄前綴正名。
  * [修復] `IS-001-02` 第一頁公司簡介替換為問卷設定之產業描述，並改列 Tier 4 歸入表單目錄。
  * [修復] Tier 1 / Tier 2 文件封面公司名稱自動套用 24 級粗體。
  * [修復] 移除打包 ZIP 內不必要的 `_output` 等測試中繼檔。
  * [新增] 實作 `questionnaire_report.py`，自動產生 `問卷填答總表.docx`。
  * [新增] 打包引擎實作 `examples/` 自動巡查機制，將範例檔併入對應目錄。
* **狀態**: Phase 6b 完成 — P2/P3 深層問卷產出機制實作
* **更新內容**:
  * [文檔] 設計產出規劃 (`p2_p3_generation_plan.md`)，並獲核准。
  * [引擎] `batch_tagger.py` 新增 10 條管理條文置換（如 BYOD、VPN、備份機制）。
  * [引擎] `document_generator.py` 新增條件排除機制（如：禁用 BYOD 則不產出相關表單）。
  * [引擎] `document_generator.py` 實作 Excel 動態預填模組，收集的「核心系統」自動逐列寫入 `IS-004-01`。
  * [測試] 11/11 E2E Workflow 測試全數通過。
* **狀態**: Phase 6 完成 — 範本驅動問卷重構
* **更新內容**:
  * [引擎] `batch_tagger.py` 新增 OOOO/OOO/XXX/○○○○○ 替換規則，全 59 份範本重新標籤化。
  * [引擎] 新增 `template_marker.py`，對 17 份操作型表單插入「⚠ 使用者須知」黃底提示。
  * [問卷] 新增 `questionnaire_config.json`，定義 20 個問卷欄位（階段一 12 題、階段二 2 題、階段三 6 題）。
  * [前端] 新增 `_stage_form.html` 可重用表單 partial，stage1/2/3 改為動態渲染。
  * [後端] `app.py` 載入 questionnaire config、新增衍生變數計算（`publish_date_short`、`dept_name`）。
  * [結構] `document_structure.json` 新增 4 個變數、移除非範本檔案（PDF/Icon/PNG）。

## v0.4.0 - 2026-03-06
* **狀態**: 交付封裝完成 (Delivery Phase) - Phase 5 完成
* **更新內容**:
  * [交付] 新增 `README.md` 系統操作手冊，包含快速啟動、專案結構、使用流程、範本修改教學、變數對照表。
  * [交付] 新增 `start.sh` 一鍵啟動腳本，自動建立 venv 與安裝依賴。
  * [交付] 新增 `requirements.txt` 凍結 5 個生產環境依賴。
  * [修正] 補齊 `files/marked/` 中缺失的 3 份 `.xlsx` 範本（IS-004-01/02、IS-010-01），範本總數 56 → 59。
  * [維護] `.gitignore` 加入 `output/`、`user_data.json`、`*.zip`。

## v0.3.0 - 2026-03-06
* **狀態**: 開發階段 (Execution Phase) - Phase 4 整合與封裝完成
* **更新內容**:
  * [核心引擎] `document_generator.py` 新增 `.xlsx` 範本替換 (openpyxl)、`generate_all()` 回傳結構化摘要、`doc_number` 依 family key 自動注入。
  * [鉤稽檢查] 新增 `integrity_checker.py`：檢查範本存在性、Tier 2 程序書完整性、可處理類型驗證。Stage 4 UI 展示檢查結果面板。
  * [導讀手冊] 新增 `readme_generator.py`：依 user_data 動態產出 `導入指引手冊.docx`。
  * [ZIP 封裝] `app.py` 加入 `zipfile` 自動壓縮 output 目錄、`/api/download` 下載路由，success 頁面新增下載按鈕與生成摘要卡片。
  * [E2E 測試] 新增 `src/tests/test_e2e.py`，11 項測試全數通過。

## v0.2.0 - 2026-03-05
* **狀態**: 開發階段 (Execution Phase) - Phase 2 & 3 核心引擎與介面完成
* **更新內容**:
  * [核心引擎] 完成 `document_generator.py` (導入 `docxtpl` 保留排版) 與 `batch_tagger.py` (支援 56 份檔案批次標籤化)。
  * [試算分析] 完成 `excel_calculator.py` 使用 `openpyxl` 進行動態風險值計算並抓出超標風險。
  * [前端介面] 使用 Flask + TailwindCSS 構建「四階段導入問卷系統」，並將使用者表單成功介接核心引擎，實現一鍵打包產生。
  * 更新進度追蹤至 `current.md` 及梳理 `walkthrough.md`。

## v0.1.4 - 2026-03-05
* **狀態**: 規劃階段 (Planning Phase) - 核心設計補強
* **更新內容**:
  * 強化問卷設計之核心精神：明訂「以範本為基礎的漸進生成 (Template-Driven Approach)」，確保所有問卷題目與邏輯皆由各階層表單反向解構而來。
  * 於 `plan.md` 的 Phase 3 加入首要步驟：執行範本解構與問答邏輯逆推。
  * 更新進度追蹤 `current.md`。

## v0.1.3 - 2026-03-05
* **狀態**: 規劃階段 (Planning Phase) - 流程對齊
* **更新內容**:
  * 依據 `workflow_design.md` 之使用者體驗藍圖，將前端開發計畫 (`plan.md`) 與系統規格 (`sys_spec.md`) 全面對齊「四階段引導流程」。
  * 於系統匯出模組新增「落地導讀手冊 (ReadMe) 動態生成」以引導終端使用者後續的紙本簽核與公告作業。
  * 更新進度追蹤 `current.md`。

## v0.1.2 - 2026-03-05
* **狀態**: 規劃階段 (Planning Phase) - 需求擴充
* **更新內容**:
  * 新增「動態內容調整與差異比對模組」：系統可依據問卷回覆，針對特定產業或公司需求，動態修改文件範文。
  * 實作變更審閱機制：在最終文件產出前，提供「預設範本」與「客製化內容」的差異比對 (Diff) 畫面，供使用者進行最終確認。
  * 更新 `sys_spec.md`、`plan.md` 與 `current.md` 反映上述流程。

## v0.1.1 - 2026-03-04
* **狀態**: 規劃階段 (Planning Phase) - 需求擴充
* **更新內容**:
  * 針對系統需求進行細部擴充，包含：
    * 支援四階層文件架構與編碼原則自動關聯。
    * 提供特定表單（如：內外部溝通管制表）之引導填寫範本。
    * 實作檢核條件與文件間鉤稽之防呆提醒機制。
    * 開發風險評鑑自動掃描、數據歸類與分析報告自動寫入機制。
  * 同步更新 `sys_spec.md`、`plan.md` 與 `current.md`。

## v0.1.0 - 2026-03-04
* **狀態**: 規劃階段 (Planning Phase)
* **更新內容**:
  * 專案正式啟動，完成初步系統需求分析討論。
  * 確立場景與使用者輪廓，以無程式背景之 ISO 27001 導入承辦人為主要受眾。
  * 建立四份基礎開發文件：
    1. `sys_spec.md` (系統規格)
    2. `current.md` (開發進度與狀態追蹤)
    3. `plan.md` (專案開發計畫與里程碑)
    4. `version.md` (版本更新紀錄)
  * 完成範本前置作業：將原先分散在資料夾中的 ISO 27001 範本檔案扁平化整理至單一 `files` 目錄，以利後續程式批次讀取。
