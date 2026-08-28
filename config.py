import os
from dotenv import load_dotenv

load_dotenv()

# Groq — bepul, kartasiz API. https://console.groq.com/keys dan oling.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# CEFR baholash uchun ishlatiladigan til modeli (Groq bepul katalogida mavjud).
GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "openai/gpt-oss-120b")

# Audio -> matn uchun ishlatiladigan Whisper modeli (Groq bepul katalogida mavjud)
GROQ_WHISPER_MODEL = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3-turbo")

# Rasm orqali yuborilgan savolni o'qish uchun ishlatiladigan vizual model
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.6-27b")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY topilmadi. Render Environment Variables'ga qo'shing.")
