from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.workflow_service import workflow_service
from app.core.prompts import PLATFORM_PROMPTS

router = APIRouter()

class CopyRequest(BaseModel):
    platform: str
    topic: str
    style: str = "專業且親切"
    model: str = "gpt-4o"
    provider: str = "openai"
    use_rag: bool = True
    use_agent: bool = False
    use_search: bool = False

class CopyResponse(BaseModel):
    content: str
    context_used: list = []
    logs: list = []

class BrainstormRequest(BaseModel):
    idea: str
    platform: str = "facebook"

@router.post("/brainstorm")
async def brainstorm_themes(request: BrainstormRequest):
    prompt = f"""
    你是一位社群媒體創意總監。使用者有一個初步的想法："{request.idea}"
    請針對 {request.platform} 平台，提供 3 個不同的貼文切入點或主題建議。
    每個建議請包含：
    1. 主題名稱
    2. 核心訴求 (為什麼這個切入點會吸引人)
    3. 建議的內容大綱
    
    請用繁體中文回答，並以 Markdown 格式呈現。
    """
    
    content = await llm_service.generate_text(
        prompt=prompt,
        system_prompt="你是一位專業的社群媒體創意總監，擅長發想引人入勝的貼文主題。",
        model="gemini-3-flash-preview",
        provider="google"
    )
    return {"suggestions": content}

@router.post("/generate", response_model=CopyResponse)
async def generate_copy(request: CopyRequest):
    if request.platform.lower() not in PLATFORM_PROMPTS:
        raise HTTPException(status_code=400, detail="Unsupported platform")
    
    context_str = ""
    context_used = []
    
    if request.use_rag:
        # Search for relevant brand knowledge
        search_results = await rag_service.query_similar("brand_knowledge", request.topic)
        if search_results:
            context_used = [res for res in search_results]
            context_str = "\n".join([res for res in search_results])
    
    if request.use_agent:
        # Use Multi-Agent Workflow
        result = await workflow_service.run_workflow(
            platform=request.platform,
            topic=request.topic,
            style=request.style,
            context=context_str,
            use_search=request.use_search
        )
        return CopyResponse(
            content=result["final_copy"],
            context_used=context_used,
            logs=result["logs"]
        )
    else:
        # Use Single LLM Call
        template = PLATFORM_PROMPTS[request.platform.lower()]
        prompt = template.format(topic=request.topic, style=request.style)
        
        if request.use_search:
            from app.services.search_service import search_service
            search_results = await search_service.search(request.topic)
            prompt = f"{prompt}\n\n最新時事資訊：\n{search_results}"
        
        if context_str:
            prompt = f"{prompt}\n\n品牌參考資訊：\n{context_str}"
        
        content = await llm_service.generate_text(
            prompt=prompt,
            model=request.model,
            provider=request.provider
        )
        
        return CopyResponse(content=content, context_used=context_used, logs=["單一 Agent 生成完成。"])
