# 券商分點買賣超爬蟲工作流程文檔

## 概述

這個 n8n 工作流程自動爬取[元富證券網站的券商分點買賣超資料](https://newjust.masterlink.com.tw/z/zg/zgb/zgb0.djhtm?a=6620&b=6620),解析 HTML 表格數據,並將結果自動記錄到 Google Sheets 試算表中。它按照每日排程運行,追蹤特定券商分點的股票交易活動。

## 工作流程組件

### 觸發器

- **Schedule Trigger（排程觸發）**：每天下午 2:00 (14:00) 自動觸發工作流程
- **When clicking 'Test workflow'（手動測試觸發）**：用於手動測試工作流程

### 數據收集

- **Code（程式碼節點）**：
  - 解析券商與分點的原始數據
  - 產生查詢 URL 列表
  - 輸出包含券商名稱、分點名稱和查詢網址的結構化資料

- **Loop Over Items（循環處理）**：將多個券商分點分批處理,避免同時發送過多請求

- **HTTP Request（HTTP 請求）**：
  - 向元富證券網站發送請求
  - URL 格式: `https://newjust.masterlink.com.tw/z/zg/zgb/zgb0.djhtm?a={券商代碼}&b={分點代碼}`
  - 以文件格式接收回應

### 數據處理

- **Extract from File（從文件提取）**：
  - 將下載的 HTML 文件轉換為文字
  - 使用 Big5-HKSCS 編碼處理繁體中文內容

- **Code1（程式碼節點1）**：
  - 解析 HTML 表格結構
  - 識別「買超」和「賣超」兩種類型的資料
  - 提取股票名稱、買進金額、賣出金額和差額
  - 處理金額格式（移除逗號,轉換為數字）

### 數據儲存

- **Google Sheets（Google 試算表）**：
  - 將解析後的數據追加到指定的 Google Sheets
  - 記錄欄位：
    - 日期（當天日期）
    - 券商名稱
    - 分點名稱
    - 類型（買超/賣超）
    - 股票名稱
    - 買進金額
    - 賣出金額
    - 差額

## 設置要求

1. **Google Sheets 配置**：
   - 準備一個 Google Sheets 試算表
   - 在 n8n 中設置 Google Sheets OAuth2 認證
   - 在 `Google Sheets` 節點中更新試算表 URL
   - 確保試算表有對應的欄位標題

2. **券商分點設置**：
   - 在 `Code` 節點中的 `raw` 變數修改要追蹤的券商與分點
   - 格式說明：
     - 使用分號 (;) 分隔不同券商群組
     - 使用驚嘆號 (!) 分隔同一券商的不同分點
     - 使用逗號 (,) 分隔代碼和名稱
   - 範例: `6010,(牛牛牛)亞證券!6012,(牛牛牛)亞-網路;6620,口袋證券;`

3. **網路連線**：
   - 確保能存取元富證券網站
   - 檢查防火牆設定

## 測試工作流程

1. 使用 `When clicking 'Test workflow'` 手動觸發節點進行測試
2. 點擊 "Test Workflow" 按鈕手動執行
3. 檢查 Google Sheets 確認數據是否正確寫入
4. 查看各節點的輸出確認解析是否正確

## 技術細節

- **編碼處理**：使用 Big5-HKSCS 編碼正確處理繁體中文網頁
- **HTML 解析**：使用正則表達式解析 HTML 表格結構
- **批次處理**：使用 Split In Batches 避免同時發送過多請求
- **循環架構**：Google Sheets 節點完成後會回到 Loop Over Items 處理下一批資料
- **日期記錄**：使用 `$today` 變數自動填入當天日期

## 自定義選項

- **時間排程**：修改 `Schedule Trigger` 節點調整執行時間（目前為每天 14:00）
- **券商列表**：在 `Code` 節點的 `raw` 變數中添加或移除券商分點
- **批次大小**：調整 `Loop Over Items` 節點的批次設定
- **試算表欄位**：在 `Google Sheets` 節點中自定義欄位對應
- **解析邏輯**：修改 `Code1` 節點中的 HTML 解析邏輯以適應不同的表格格式

## 工作流程圖

工作流程按以下順序進行：

1. **觸發階段**: Schedule Trigger / When clicking 'Test workflow' → Code
2. **批次處理**: Code → Loop Over Items → HTTP Request
3. **資料解析**: HTTP Request → Extract from File → Code1
4. **資料儲存**: Code1 → Google Sheets → Loop Over Items (循環)

## 注意事項

- 確保網站結構未改變,若元富證券網站更新 HTML 格式,需要相應調整 `Code1` 節點的解析邏輯
- 建議在交易日收盤後執行,確保數據完整
- 注意 API 請求頻率,避免對目標網站造成過大負擔
- Google Sheets API 有每日配額限制,大量數據時需注意

## 數據應用

收集的數據可用於：
- 分析特定券商分點的交易行為
- 追蹤主力進出動向
- 識別熱門標的
- 建立交易策略參考指標
