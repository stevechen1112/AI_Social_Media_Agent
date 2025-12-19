# AI 社群文案 Agent - 完整系統開發計畫書

## 1. 專案概述
本計畫旨在開發一套全功能的 AI 社群媒體代理人（AI Social Media Agent），專注於為 Facebook、Instagram、Threads 自動生成高品質、符合平台特性且具備品牌風格的貼文內容。系統將不只是簡單的文字生成器，而是包含多 Agent 協作、視覺理解、品牌記憶（RAG）與聯網能力的完整工作流系統。

## 2. 推薦技術棧 (Tech Stack)

*   **前端 (Frontend):** Next.js (React), Tailwind CSS, Shadcn/UI (現代化 UI/UX)
*   **後端 (Backend):** Python (FastAPI) - 適合處理 AI 邏輯與異步任務
*   **AI 核心 (AI Core):**
    *   **Orchestration:** LangChain 或 LangGraph (處理複雜工作流)
    *   **LLM Models:** GPT-4o (邏輯與多模態), Claude 3.5 Sonnet (文案撰寫)
    *   **Multi-Agent:** LangGraph 或 CrewAI
*   **資料庫 (Database):**
    *   **Relational:** PostgreSQL (Supabase) - 儲存使用者資料、貼文歷史
    *   **Vector DB:** Pinecone 或 Supabase pgvector - 儲存品牌風格庫 (RAG)
*   **其他:** Docker (部署), Redis (快取與任務隊列)

---

## 3. 分階段開發計畫 (Phased Development Plan)

我們將開發分為五個階段，確保系統架構穩健並逐步堆疊進階功能。

### Phase 1: 基礎建設與核心生成引擎 (Foundation & Core Generation)
**目標：** 建立前後端架構，實現針對 FB/IG/Threads 的差異化文案生成。
*   搭建 Next.js + FastAPI 專案骨架。
*   設計 Prompt Template 系統，針對三平台定義不同風格參數。
*   實作基本的 LLM 串接 (OpenAI/Anthropic)。
*   建立使用者帳戶系統 (Supabase Auth)。
*   **產出：** 一個可以登入、選擇平台、輸入主題並獲得差異化文案的 Web App。

### Phase 2: 品牌大腦與 RAG 系統 (Brand Brain & RAG)
**目標：** 讓 Agent 能夠「記住」並「模仿」使用者的品牌語氣。
*   建立向量資料庫 (Vector DB)。
*   開發「知識庫上傳」功能：使用者上傳過去的高讚貼文、品牌手冊 (PDF/Text)。
*   實作 RAG (Retrieval-Augmented Generation) 流程：生成文案前先檢索相似風格的歷史貼文作為參考 (Few-shot prompting)。
*   **產出：** Agent 寫出的文案不再是通用的機器人語氣，而是具備特定品牌調性。

### Phase 3: 多模態視覺理解 (Multimodal Capabilities)
**目標：** 支援「看圖寫文」，解決使用者不知如何描述圖片的痛點。
*   整合 GPT-4o 或 Gemini 1.5 Pro 的視覺能力。
*   開發圖片上傳與分析模組：自動提取圖片中的物件、氛圍、顏色、文字。
*   將視覺資訊轉化為 Prompt 的一部分，生成與圖片高度相關的文案。
*   (選配) 整合 DALL-E 3 或 Midjourney API 進行反向操作：根據文案生成配圖建議。
*   **產出：** 使用者上傳產品圖，Agent 自動產出 IG 貼文與 Hashtag。

### Phase 4: 多 Agent 協作工作流 (Multi-Agent Workflow)
**目標：** 引入「編輯部」概念，提升文案品質與多樣性。
*   利用 LangGraph 構建多 Agent 狀態機。
*   **角色定義：**
    *   **Planner:** 分析主題，決定切入點與結構。
    *   **Writer:** 根據 Planner 指示撰寫初稿。
    *   **Editor:** 審查初稿，檢查是否符合品牌規範、有無幻覺、語氣是否自然。
    *   **Critique:** 模擬酸民或嚴格讀者，提出修改建議。
*   **產出：** 經過多輪自我修正的高品質文案，減少人工潤飾時間。

### Phase 5: 聯網能力與外部整合 (Web Search & Integration)
**目標：** 讓文案結合時事，並優化輸出體驗。
*   整合搜尋工具 (Tavily API 或 Google Search API)。
*   實作「趨勢偵測」：Agent 自動搜尋當下熱門 Hashtag 或新聞梗。
*   (進階) 嘗試串接 FB/IG Graph API (需經過 Meta 審核)，實現排程發布或草稿預覽。
*   **產出：** 具備時事敏感度的 Agent，以及更流暢的發布流程。

---

## 4. 詳細任務清單 (Task Plan)

### Phase 1: 基礎建設
- [x] **[Infra]** 初始化 Next.js 前端專案 (Tailwind, Shadcn)。
- [x] **[Infra]** 初始化 FastAPI 後端專案 (Poetry/Pipenv)。
- [x] **[Infra]** 設定 Supabase 專案 (Auth, Database)。
- [x] **[Backend]** 設計資料庫 Schema (Users, Posts, Templates)。
- [x] **[Backend]** 封裝 OpenAI/Claude API Client。
- [x] **[AI]** 撰寫 FB/IG/Threads 基礎 Prompt Templates (v1.0)。
- [x] **[Frontend]** 開發主儀表板 (Dashboard) 與文案生成表單。
- [x] **[Frontend]** 實作 Markdown 渲染與「一鍵複製」功能。

### Phase 2: RAG 品牌腦
- [x] **[Backend]** 設定 Vector Database (Pinecone/Supabase)。
- [x] **[Backend]** 開發文件解析器 (PDF/Txt/CSV loader)。
- [x] **[Backend]** 實作 Embedding 流程 (OpenAI Embeddings)。
- [x] **[AI]** 優化 Prompt 流程，加入 Context Retrieval (RAG)。
- [x] **[Frontend]** 開發「品牌設定」頁面，允許上傳範例貼文。
- [x] **[Frontend]** 顯示 RAG 檢索到的參考來源 (增加可信度)。

### Phase 3: 多模態視覺
- [x] **[Backend]** 實作圖片上傳 API (S3 或 Supabase Storage)。
- [x] **[AI]** 串接 GPT-4o Vision API 進行圖片分析。
- [x] **[AI]** 設計「圖片 -> 文案」的專屬 Prompt Chain。
- [x] **[Frontend]** 整合圖片上傳元件與預覽功能。
- [x] **[AI]** (Optional) 實作 IG Hashtag 生成器 (基於圖片內容)。

### Phase 4: 多 Agent 協作
- [x] **[AI]** 引入 LangGraph 框架。
- [x] **[AI]** 定義 Agent State (狀態) 與 Graph (流程圖)。
- [x] **[AI]** 實作 Planner Agent (搜尋靈感/決定架構)。
- [x] **[AI]** 實作 Editor Agent (評分與修改建議)。
- [x] **[Backend]** 將單一 API 呼叫改為 Streaming Response (顯示各 Agent 工作狀態)。
- [x] **[Frontend]** UI 優化：顯示「思考過程」與多版本比較。

### Phase 5: 聯網與優化
- [x] **[AI]** 整合 Tavily Search API。
- [x] **[AI]** 設計「時事結合」模式的 Prompt。
- [x] **[Backend]** 實作 Redis Queue 處理長時任務。
- [x] **[System]** 進行壓力測試與 Token Cost 分析。
- [x] **[System]** 撰寫 API 文件與部署腳本 (Docker Compose)。
