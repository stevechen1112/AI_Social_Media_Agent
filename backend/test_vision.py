import asyncio
import os
import base64
import io
from PIL import Image
from dotenv import load_dotenv
from app.services.llm_service import llm_service

# Load environment variables
load_dotenv()

async def test_vision():
    print("👁️ Testing Vision with Gemini 3 Flash Preview...")
    
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color = 'red')
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    image_url = f"data:image/jpeg;base64,{img_str}"
    
    print("📸 Generated dummy image (Red Square)")
    
    try:
        # Force provider to google implicitly by not having OpenAI key or by logic
        # The current logic tries OpenAI first, then Google.
        # If OpenAI key is missing (which it is in .env), it falls back to Google.
        
        response = await llm_service.analyze_image(
            image_url=image_url,
            prompt="What color is this image? Please answer in one word."
        )
        print(f"\n✅ Vision Analysis Result:\n{response}")
    except Exception as e:
        print(f"\n❌ Vision Analysis failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_vision())
