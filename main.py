"""
CEFR Multilevel Test - Backend API
Speaking va Writing baholash uchun asosiy server.

Ishga tushirish (lokal test uchun):
    uvicorn main:app --reload --port 8000

Deploy qilinganda (Render.com) start command:
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""

import os
import uuid
import shutil
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CEFR Test API")

# Frontend istalgan manzildan so'rov yubora olishi uchun (Telegram Mini App uchun kerak)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# TASK PROMPTLARI (hozircha shu yerda, keyinchalik bazaga ko'chirish mumkin)
# ---------------------------------------------------------------------------
WRITING_TASKS = {
    "task1_1": {
        "title": "Task 1.1",
        "prompt": "BU YERGA TASK 1.1 MATNINI YOZING (masalan: rasmiy xat yozish topshirig'i)",
        "time_limit_min": 20,
    },
    "task1_2": {
        "title": "Task 1.2",
        "prompt": "BU YERGA TASK 1.2 MATNINI YOZING",
        "time_limit_min": 20,
    },
    "essay": {
        "title": "Essay / Blog post",
        "prompt": "BU YERGA ESSAY/BLOG POST MAVZUSINI YOZING",
        "time_limit_min": 40,
    },
}


# ---------------------------------------------------------------------------
# TASKLARNI OLISH
# ---------------------------------------------------------------------------
@app.get("/api/tasks")
async def get_tasks():
    """Frontend sahifa ochilganda shu yerdan barcha topshiriqlarni oladi."""
    return WRITING_TASKS


# ---------------------------------------------------------------------------
# SPEAKING: audio yuklash (yozib olingan HAM, tayyor fayl HAM shu endpointga keladi)
# ---------------------------------------------------------------------------
@app.post("/api/submit-speaking")
async def submit_speaking(
    audio: UploadFile = File(...),
    user_id: str = Form(...),
    part: str = Form("part1"),  # masalan: part1, part2, part3 - CEFR speaking qismlari
):
    # 1) Faylni saqlaymiz
    ext = os.path.splitext(audio.filename)[1] or ".ogg"
    filename = f"{user_id}_{part}_{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    # 2) TODO: Shu yerga sizning botingizdagi mavjud logikani qo'yasiz:
    #    a) Audio -> matn (masalan Whisper API orqali)
    #    b) Matn -> CEFR baholash (GPT/Claude promptingiz orqali)
    #
    #    Masalan:
    #    transcript = transcribe_audio(filepath)
    #    result = evaluate_speaking_cefr(transcript, part=part)

    # Hozircha vaqtinchalik (mock) natija qaytaramiz - buni keyin almashtiramiz
    result = {
        "status": "ok",
        "transcript": "(bu yerda audio matnga aylantirilgan holda chiqadi)",
        "cefr_level": "B2",
        "feedback": "Bu vaqtinchalik test natijasi. Haqiqiy baholash logikasi hali ulanmagan.",
        "scores": {
            "fluency": 0,
            "vocabulary": 0,
            "grammar": 0,
            "pronunciation": 0,
        },
    }

    return result


# ---------------------------------------------------------------------------
# WRITING: matn HAM, fayl (docx/pdf/txt) HAM shu endpointga keladi
# ---------------------------------------------------------------------------
@app.post("/api/submit-writing")
async def submit_writing(
    task_id: str = Form(...),          # "task1_1" | "task1_2" | "essay"
    user_id: str = Form(...),
    text: Optional[str] = Form(None),  # to'g'ridan-to'g'ri yozilgan matn
    file: Optional[UploadFile] = File(None),  # yuklangan fayl (docx/pdf/txt)
):
    if task_id not in WRITING_TASKS:
        raise HTTPException(status_code=400, detail="Noto'g'ri task_id")

    final_text = text or ""

    # Agar fayl yuborilgan bo'lsa - avval saqlaymiz, keyin matnga aylantiramiz
    if file is not None:
        ext = os.path.splitext(file.filename)[1].lower()
        filename = f"{user_id}_{task_id}_{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)

        final_text = extract_text_from_file(filepath, ext)

    if not final_text.strip():
        raise HTTPException(status_code=400, detail="Matn yoki fayl bo'sh")

    # TODO: Shu yerga sizning botingizdagi mavjud Writing baholash promptini qo'yasiz
    # result = evaluate_writing_cefr(final_text, task_id=task_id)

    result = {
        "status": "ok",
        "task": WRITING_TASKS[task_id]["title"],
        "word_count": len(final_text.split()),
        "cefr_level": "B2",
        "feedback": "Bu vaqtinchalik test natijasi. Haqiqiy baholash logikasi hali ulanmagan.",
        "scores": {
            "task_achievement": 0,
            "coherence": 0,
            "vocabulary": 0,
            "grammar": 0,
        },
    }

    return result


# ---------------------------------------------------------------------------
# Yordamchi funksiya: fayldan matn chiqarish (docx / pdf / txt)
# ---------------------------------------------------------------------------
def extract_text_from_file(filepath: str, ext: str) -> str:
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif ext == ".docx":
        import docx  # python-docx
        doc = docx.Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    elif ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    else:
        raise HTTPException(status_code=400, detail=f"Qo'llab-quvvatlanmaydigan fayl turi: {ext}")


@app.get("/")
async def root():
    return {"message": "CEFR Test API ishlayapti ✅"}
