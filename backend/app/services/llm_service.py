from typing import Optional
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
import base64
import io
from PIL import Image
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
        
        self.google_available = False
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.google_available = True

    async def generate_text(
        self, 
        prompt: str, 
        system_prompt: str = "You are a helpful social media assistant.",
        model: str = "gpt-4o",
        provider: str = "openai"
    ) -> str:
        # Auto-fallback logic
        if provider == "openai" and not self.openai_client:
            if self.google_available:
                provider = "google"
                model = "gemini-3-flash-preview"
            elif self.anthropic_client:
                provider = "anthropic"
                model = "claude-3-sonnet-20240229"

        if provider == "openai":
            if not self.openai_client:
                return "OpenAI API key not configured."
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        
        elif provider == "anthropic":
            if not self.anthropic_client:
                return "Anthropic API key not configured."
            
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
            
        elif provider == "google":
            if not self.google_available:
                return "Google API key not configured."
            
            # Use gemini-3-flash-preview by default if model is gpt-4o or other provider specific
            if not model.startswith("gemini"):
                model = "gemini-3-flash-preview"
                
            model_instance = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_prompt
            )
            response = model_instance.generate_content(prompt)
            return response.text
        
        return "Unsupported provider."

    async def analyze_image(self, image_url: str, prompt: str = "請描述這張圖片的內容、氛圍、顏色以及適合的社群媒體主題。") -> str:
        # Try OpenAI first
        if self.openai_client:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )
            return response.choices[0].message.content
            
        # Fallback to Google
        if self.google_available:
            try:
                # Parse data URI
                if image_url.startswith("data:image"):
                    header, encoded = image_url.split(",", 1)
                    data = base64.b64decode(encoded)
                    image = Image.open(io.BytesIO(data))
                    
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    response = model.generate_content([prompt, image])
                    return response.text
                else:
                    return "Image URL format not supported for Google provider (only data URI)."
            except Exception as e:
                return f"Google Vision analysis failed: {str(e)}"

        return "No Vision API provider configured (OpenAI or Google)."

llm_service = LLMService()
