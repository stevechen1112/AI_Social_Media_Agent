import os
from tavily import TavilyClient
from app.core.config import settings

class SearchService:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY", "")
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None

    async def search(self, query: str, search_depth: str = "basic"):
        if not self.client:
            return "Tavily API key not configured."
        
        # Tavily's search is synchronous, but we can wrap it if needed. 
        # For simplicity in this async environment:
        response = self.client.search(query=query, search_depth=search_depth)
        
        results = []
        for result in response.get("results", []):
            results.append(f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n")
        
        return "\n---\n".join(results)

search_service = SearchService()
