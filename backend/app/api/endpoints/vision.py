from fastapi import APIRouter, UploadFile, File, HTTPException
import base64
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    print(f"📸 Receiving image analysis request: {file.filename}")
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["jpg", "jpeg", "png", "webp"]:
        print(f"❌ Unsupported image type: {file_ext}")
        raise HTTPException(status_code=400, detail="Unsupported image type")
    
    # Read file and convert to base64
    try:
        contents = await file.read()
        print(f"📦 Image size: {len(contents)} bytes")
        base64_image = base64.b64encode(contents).decode('utf-8')
        image_url = f"data:image/{file_ext};base64,{base64_image}"
        
        prompt = """
        你是一位專業的社群媒體視覺分析師。請分析這張圖片並提供以下資訊：
        1. 圖片內容描述 (Objects, Scene)
        2. 氛圍與情緒 (Mood, Emotion)
        3. 主要顏色與視覺風格
        4. 適合的社群媒體貼文主題建議
        5. 建議的 5 個 Hashtags
        
        請用繁體中文回答。
        """
        
        print("🤖 Sending to LLM for analysis...")
        analysis = await llm_service.analyze_image(image_url, prompt)
        print("✅ Analysis complete.")
        return {"analysis": analysis}
    except Exception as e:
        print(f"❌ Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
