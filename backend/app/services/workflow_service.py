from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, END
from app.services.llm_service import llm_service
from app.services.search_service import search_service
from app.core.prompts import PLATFORM_PROMPTS

class AgentState(TypedDict):
    platform: str
    topic: str
    style: str
    context: str
    search_results: str
    use_search: bool
    plan: str
    draft: str
    critique: str
    final_copy: str
    revision_count: int
    logs: Annotated[List[str], operator.add]

class WorkflowService:
    def __init__(self):
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("searcher", self.searcher_node)
        workflow.add_node("planner", self.planner_node)
        workflow.add_node("writer", self.writer_node)
        workflow.add_node("editor", self.editor_node)

        # Define edges
        workflow.set_entry_point("searcher")
        workflow.add_edge("searcher", "planner")
        workflow.add_edge("planner", "writer")
        workflow.add_edge("writer", "editor")
        
        workflow.add_conditional_edges(
            "editor",
            self.should_continue,
            {
                "continue": "writer",
                "end": END
            }
        )

        return workflow.compile()

    async def searcher_node(self, state: AgentState):
        if not state.get("use_search"):
            return {"search_results": "", "logs": ["Searcher: 跳過聯網搜尋。"]}
        
        query = f"最新關於 {state['topic']} 的趨勢與新聞"
        results = await search_service.search(query)
        return {
            "search_results": results,
            "logs": ["Searcher: 已完成聯網搜尋，獲取最新時事資訊。"]
        }

    async def planner_node(self, state: AgentState):
        prompt = f"""
        你是一位社群媒體策略師。請針對以下主題與平台，規劃貼文的結構與重點。
        平台：{state['platform']}
        主題：{state['topic']}
        風格：{state['style']}
        品牌背景：{state['context']}
        聯網搜尋結果：{state.get('search_results', '無')}
        
        請輸出貼文的規劃大綱，並嘗試結合搜尋到的時事資訊（如果有）。
        """
        plan = await llm_service.generate_text(prompt, system_prompt="你是一位專業的社群媒體策略師。")
        return {
            "plan": plan,
            "logs": ["Planner: 已完成貼文結構規劃（已結合時事資訊）。"]
        }

    async def writer_node(self, state: AgentState):
        template = PLATFORM_PROMPTS.get(state['platform'].lower(), "{topic}")
        prompt = f"""
        根據以下規劃大綱撰寫貼文：
        規劃大綱：{state['plan']}
        
        品牌背景：{state['context']}
        風格要求：{state['style']}
        
        請撰寫正式的貼文內容。
        """
        if state.get('critique'):
            prompt += f"\n\n請參考以下修改建議進行優化：\n{state['critique']}"
            
        draft = await llm_service.generate_text(prompt, system_prompt="你是一位擅長撰寫社群文案的作家。")
        return {
            "draft": draft,
            "logs": [f"Writer: 已生成第 {state.get('revision_count', 0) + 1} 版草稿。"]
        }

    async def editor_node(self, state: AgentState):
        prompt = f"""
        你是一位嚴格的社群媒體編輯。請審查以下貼文草稿：
        草稿：{state['draft']}
        
        審查標準：
        1. 是否符合平台 {state['platform']} 的特性？
        2. 語氣是否符合 {state['style']}？
        3. 是否有錯字或語句不通順？
        
        如果草稿已經非常完美，請回覆 "PASS"。
        如果需要修改，請提供具體的修改建議。
        """
        critique = await llm_service.generate_text(prompt, system_prompt="你是一位專業的社群媒體編輯。")
        
        revision_count = state.get('revision_count', 0) + 1
        
        if "PASS" in critique.upper() or revision_count >= 2:
            return {
                "final_copy": state['draft'],
                "revision_count": revision_count,
                "logs": ["Editor: 審核通過，文案已定稿。"]
            }
        else:
            return {
                "critique": critique,
                "revision_count": revision_count,
                "logs": [f"Editor: 提出修改建議：{critique[:50]}..."]
            }

    def should_continue(self, state: AgentState):
        if state.get("final_copy"):
            return "end"
        return "continue"

    async def run_workflow(self, platform: str, topic: str, style: str, context: str = "", use_search: bool = False):
        initial_state = {
            "platform": platform,
            "topic": topic,
            "style": style,
            "context": context,
            "use_search": use_search,
            "revision_count": 0,
            "logs": []
        }
        result = await self.workflow.ainvoke(initial_state)
        return result

workflow_service = WorkflowService()
