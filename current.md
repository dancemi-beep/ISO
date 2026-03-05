# 目前開發進度與狀態 (Current Status)

**最後更新時間：** 2026-03-04

## 1. 目前完成事項
* [x] 確立專案目標與系統規格 (撰寫 `sys_spec.md`)。
* [x] 規劃專案開發進度與拆解任務 (撰寫 `plan.md`)。
* [x] 建立版本控制與紀錄文件 (`version.md`)。
* [x] 將原先 `導入文件` 內的各項 ISO 27001 範本檔案扁平化整理至 `files` 目錄，以便後續程式讀取。

## 2. 當前開發階段
* **階段 2：系統核心生成邏輯 (Core Engine) (進行中)**
* 目前狀態：✅ **完成階段 1 概念驗證 (POC)**
  * 環境建立：已建立 Python `venv` 並安裝 `python-docx`。
  * 驗證腳本：成功撰寫 `prepare_template.py`（動態打標籤）與 `generate_poc.py`（填寫變數）
  * 測試結果：順利將「IS-001 資訊安全政策」變數替換為真實資料並另存新檔。
  * **POC 優化需求 (未來擴充點)**：
    1. 需支援讀取外部 `JSON` 設定檔進行動態變數注入。
    2. 需要具備遍歷 `files` 目錄並「批次生成」多階層文件的能力。
    3. `paragraph.text` 全部替換可能導致 Word 原有樣式遺失，需實作更穩定、能保留樣式屬性 (Runs formatting) 的標籤替換演算法。

## 3. 下一步工作 (Next Steps)
1. **[已完成] 盤點四階層文件與變數**：檢視 `files` 目錄，完成 `document_structure.json` 並注入共通變數。
2. **[已完成] 批次生成模組**：採用 `docxtpl` (基於 Jinja2) 實作了強健的替換機制 (`src/engine/document_generator.py`)，成功保留 Word 原生樣式，並支援讀取結構 JSON 進行批次處理。
3. **[已完成] 檔案全面標籤化 (Jinja Regex)**：撰寫 `src/engine/batch_tagger.py`，成功將 `files` 內所有的 `.docx` 檔案 (約 56 份) 裡面的預設字眼（如「XXXX股份有限公司」、「年/月/日」）大量替換成 `{{ company_name }}` 等變數字串，並儲存於 `files/marked/` 目錄中。
4. **[已完成] 加入 Excel 驗證**：建立 `src/poc/excel_calculator.py`，使用 `openpyxl` 成功讀寫 `.xlsx`，並能針對「IS-004-01資產及風險評鑑表」進行讀取、風險值運算與高風險資產門檻篩選的 POC 證明。

## 4. 待確認事項或阻礙
* **Phase 3 (四階段導引前端介面) 已全數驗證完成。**
* 系統現在能夠完全透過網頁介面引導使用者輸入參數，並於背景順暢呼叫 `document_generator.py` 一鍵產出 56 份客製化之 ISO 27001 文件與風險評鑑表。
* 接下來可以進行 Phase 4/5：測試整合與交付封裝。
