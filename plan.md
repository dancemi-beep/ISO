# ISO 27001 ISMS 導入文件生成系統 - 開發計畫 (Development Plan)

## 專案開發里程碑 (Milestones)

### Phase 1: 基礎環境準備與概念驗證 ✅
### Phase 2: 系統核心生成邏輯 ✅
### Phase 3: 四階段導引之前端介面開發 ✅
### Phase 4: 系統整合、鉤稽檢查與最終封裝 ✅
### Phase 5: 使用者手冊與專案交付 ✅

---

### Phase 6: 範本驅動問卷重構與標記強化 (Template-Driven Questionnaire Redesign)
* **目標**: 讓問卷問題 100% 對應範本內容，達成「答完題即寫完文件」。
* **步驟**:
  1. [ ] **6.1 補完標籤化**：修正 `batch_tagger.py` 替換規則，補上 `OOOO`/`OOO`/`XXX` → Jinja 變數，重新處理 7 份未完成標籤化的文件。
  2. [ ] **6.2 操作型表單標記**：撰寫 `template_marker.py`，對 15 份含 □/___/表格 的操作型表單插入醒目「⚠ 待修改」提示段落。
  3. [ ] **6.3 問卷欄位逆推**：逐一審閱 59 份範本，為每份文件定義 `questionnaire_fields`，更新 `document_structure.json`。
  4. [ ] **6.4 前端動態化**：修改 `app.py` 與 stage HTML 模板，改為依據 `questionnaire_fields` 動態產出表單。
  5. [ ] **6.5 驗證**：E2E 測試 + 手動抽查。
