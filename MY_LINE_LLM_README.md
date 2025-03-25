# MY LINE LLM

一個簡單的 LINE 聊天機器人，整合 Google Gemini AI 模型，使用 n8n 工作流平台構建。

## 功能概述

- 接收用戶透過 LINE 發送的文字訊息
- 使用 Google Gemini AI 處理訊息
- 以繁體中文回覆用戶

## 設置指南

### LINE 平台設置

1. 登入 [LINE Developers Console](https://developers.line.biz/console/)
2. 創建新的提供者（Provider）
3. 創建 Messaging API 頻道
4. 獲取 Channel Access Token
5. 設置 Webhook URL: `https://您的域名/webhook/line-message`
6. 關閉自動回覆和問候訊息
7. 掃描 QR Code 將機器人添加為好友

### n8n 設置

1. 安裝並啟動 n8n
   ```
   npm install n8n -g
   n8n start
   ```

2. 導入 MY_LINE_LLM.json 工作流
3. 配置以下憑證:
   - LINE Channel Access Token (HTTP Header Auth)
   - Google Gemini API 密鑰

4. 啟用工作流

## 工作流說明

工作流包含以下節點:

1. **Webhook**: 接收 LINE 平台的訊息
2. **Code**: 解析 LINE 訊息內容
3. **Google Gemini Chat Model**: AI 語言模型
4. **Basic LLM Chain**: 處理用戶輸入
5. **Code1**: 處理 AI 回覆格式
6. **HTTP Request**: 發送回覆到 LINE
7. **Respond to Webhook**: 完成請求處理

## 常見問題

- **沒有收到回覆**: 檢查 Channel Access Token 和 Webhook URL
- **回覆格式錯誤**: 檢查 Code1 節點中的文本處理邏輯
- **無法連接 Google Gemini**: 確認 API 密鑰是否有效

## 參考資源

- [LINE Messaging API 文檔](https://developers.line.biz/en/docs/messaging-api/)
- [n8n 文檔](https://docs.n8n.io/)
- [Google Gemini API 文檔](https://ai.google.dev/docs)
