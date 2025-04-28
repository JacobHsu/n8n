# n8n_tv_chart_img

## 簡介
這是一個 n8n workflow，可以自動產生 TradingView 技術分析圖（含 Keltner Channel、MACD），用 AI 分析圖表後，給出操作建議，並把圖表和建議發送到 Telegram。

---

## 功能特色
- 支援定時或手動觸發
- 自動產生幣種/股票技術分析圖
- 用 AI 讀圖並給出操作建議
- 圖片和建議自動推送到 Telegram

---

## 流程說明
1. 觸發（定時或外部呼叫）
2. 設定查詢標的（如 ETHUSDT）
3. 產生技術分析圖表
4. 下載圖表圖片
5. 用 AI 分析圖表
6. 發送圖片和建議到 Telegram

---

## 主要節點
- **Schedule Trigger**：定時執行
- **Edit Fields**：設定查詢的 ticker
- **HTTP Chart URL**：產生圖表
- **HTTP Download Chart**：下載圖表圖片
- **OpenAI**：AI 分析圖表
- **Telegram Photo / Msg**：發送圖片和建議到 Telegram

---

## 安裝與設定
1. 在 n8n 匯入 `n8n_tv_chart_img.json`
2. 準備好以下金鑰並填入對應節點：
   - chart-img API Key
   - OpenAI API Key
   - Telegram Bot Token
3. 設定 Telegram chatId
4. 如需更換查詢標的，請在 `Edit Fields` 節點修改 ticker

---

## 常見問題
- **API 金鑰錯誤**：請確認金鑰正確填入
- **Telegram 無法推送**：請確認 Bot 已加入群組並取得 chatId
- **圖表產生失敗**：請檢查 chart-img API Key 是否有效

---

## 範例
查詢 ETHUSDT，會自動產生 15 分鐘 K 線圖，AI 分析後給出操作建議，並推送到 Telegram。

---

## 參考連結
- [n8n 官方文件](https://docs.n8n.io/)
- [chart-img API](https://docs.chart-img.com/)
- [OpenAI Vision](https://platform.openai.com/docs/guides/vision)
- [Telegram Bot API](https://core.telegram.org/bots/api)