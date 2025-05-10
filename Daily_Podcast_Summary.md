# 每日播客摘要工作流程文檔

## 概述

這個n8n工作流程自動從台灣播客排行榜獲取指定類型的熱門播客，下載音頻文件，進行轉錄，生成中文摘要，並將結果發送到您的電子郵箱。它按照每日計劃運行，為您提供有關熱門播客內容的定期更新。

## 工作流程組件

### 觸發器

- **Schedule（計劃）**：每天上午8:00觸發工作流程。

### 數據收集

- **Genre（類型）**：設置要搜索的播客類型（預設：BUSINESS_INVESTING商業投資）。
- **TaddyTopDaily**：向Taddy.org發送API請求，獲取台灣指定類型的前2個熱門播客。
- **Split Out（分離）**：將播客劇集分離出來進行單獨處理。
- **Download Podcast（下載播客）**：下載完整的播客音頻文件。

### 音頻處理

- **Request Audio Crop（請求音頻裁剪）**：將音頻發送到Aspose API進行裁剪（提取8:00-24:00分鐘的內容）。
- **Get Download Link（獲取下載鏈接）**：獲取裁剪後音頻的下載鏈接。
- **If Downloads Ready（如果下載準備就緒）**：檢查下載鏈接是否可用。
- **Wait（等待）**：如果未準備就緒，則等待下載完成。
- **Download Cut MP3（下載裁剪的MP3）**：下載裁剪後的音頻文件。

### 內容分析

- **Whisper Transcribe Audio（Whisper轉錄音頻）**：使用OpenAI的Whisper模型轉錄播客音頻。
- **Summarize Podcast（播客摘要）**：使用OpenAI的GPT-4o-mini生成播客內容的簡潔中文摘要。
- **Final Data（最終數據）**：將播客信息和摘要格式化為結構化JSON對象。

### 電子郵件生成

- **Merge Results（合併結果）**：將所有播客數據合併為單個對象。
- **HTML**：創建包含播客信息和摘要的HTML表格電子郵件。
- **Gmail**：以"Podcast Review"為主題將電子郵件發送到指定的電子郵件地址。

## 設置要求

1. **Taddy API訪問**：
   - 在[Taddy.org](https://taddy.org/signup/developers)創建免費API密鑰
   - 使用您的用戶ID和API密鑰更新`TaddyTopDaily`節點

2. **Gmail配置**：
   - 按照[Google指南](https://developers.google.com/workspace/guides/create-credentials)創建訪問憑證
   - 在`Gmail`節點中使用*client_secret.json*中的憑證
   - 在`Gmail`節點中更新收件人電子郵件地址

3. **OpenAI API密鑰**：
   - 提供您的OpenAI API密鑰用於轉錄和摘要服務

4. **播客類型選擇**：
   - 修改`Genre`節點以選擇您喜歡的播客類型
   - 可用類型包括：TECHNOLOGY（技術）、NEWS（新聞）、ARTS（藝術）、COMEDY（喜劇）、SPORTS（體育）、FICTION（小說）等
   - 完整列表請參考Taddy API文檔

## 測試工作流程

1. 用`Test Workflow`（測試工作流程）節點替換`Schedule`節點
2. 點擊"Test Workflow"手動運行
3. 檢查您的電子郵件查看結果

## 技術細節

- 工作流程使用Aspose的音頻裁剪服務從每個播客中提取16分鐘的片段
- 使用OpenAI的Whisper模型進行準確的音頻轉錄
- GPT-4o-mini生成簡潔的繁體中文摘要
- 電子郵件格式為HTML表格，包含播客名稱、劇集標題（作為鏈接）和摘要
- 每個摘要限制為3-4段，重點關注關鍵信息

## 自定義選項

- **時間安排**：修改`Schedule`節點以更改發送電子郵件的時間
- **播客片段**：調整`Request Audio Crop`節點中的時間範圍（目前設置為8:00-24:00分鐘）
- **摘要長度**：更改`Summarize Podcast`節點中的`maxTokens`參數
- **電子郵件格式**：自定義`HTML`節點中的HTML模板
- **播客數量**：調整`TaddyTopDaily`節點查詢中的`limitPerPage`參數

## 工作流程圖

工作流程按以下順序進行：
1. Schedule → Genre → TaddyTopDaily → Split Out → Download Podcast
2. Download Podcast → Request Audio Crop → Get Download Link → If Downloads Ready
3. If Downloads Ready → Download Cut MP3 → Whisper Transcribe Audio → Summarize Podcast → Final Data
4. Final Data → Merge Results → HTML → Gmail
