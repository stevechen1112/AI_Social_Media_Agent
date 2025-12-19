# AI Social Media Agent 🚀

這是一個全方位的 AI 社群媒體文案助手，整合了 **RAG (品牌大腦)**、**視覺理解 (AI 看圖)**、**多 Agent 協作工作流** 以及 **聯網搜尋** 功能。

## 🌟 核心功能

1.  **文案生成 (Phase 1)**: 支援 Facebook、Instagram 與 Threads 的專屬文案生成。
2.  **品牌大腦 (Phase 2)**: 透過 RAG 技術，上傳品牌資料後，AI 能根據品牌知識撰寫文案。
3.  **視覺理解 (Phase 3)**: 上傳廣告圖或產品照，AI 自動分析圖片內容並建議貼文方向。
4.  **多 Agent 協作 (Phase 4)**: 模擬編輯部流程（規劃 -> 撰寫 -> 潤飾），提升文案品質。
5.  **聯網搜尋 (Phase 5)**: 整合 Tavily 搜尋，讓文案能結合最新時事與趨勢。

## 🛠️ 技術棧

-   **前端**: Next.js 14, Tailwind CSS, Shadcn/UI
-   **後端**: FastAPI (Python), Poetry
-   **AI 模型**: Google Gemini 3 Flash (Preview), OpenAI GPT-4o (Vision)
-   **向量資料庫**: ChromaDB (本地端)
-   **工作流**: LangGraph

## 🚀 快速開始

### 1. 環境設定

在 `backend` 資料夾中建立 `.env` 檔案：

```env
GOOGLE_API_KEY=你的_GEMINI_API_KEY
TAVILY_API_KEY=你的_TAVILY_API_KEY
```

### 2. 啟動後端 (FastAPI)

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### 3. 啟動前端 (Next.js)

```bash
cd frontend
npm install
npm run dev
```

打開瀏覽器前往 [http://localhost:3000](http://localhost:3000) 即可開始使用。

## 📝 開發計畫

詳細開發進度請參考 [AI_Social_Media_Agent_Dev_Plan.md](./AI_Social_Media_Agent_Dev_Plan.md)。
