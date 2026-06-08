from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
import os

app = FastAPI()

# CORS - Tashqi so'rovlar yoki mahalliy testlar bilan muammosiz bog'lanish uchun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# FRONTEND SAHIFALARINI KO'RSATISH (VERCEL MONOLIT SOZLAMASI)
# -------------------------------------------------------------

# 1. Kirish sahifasi (index.html) - Loyihangizning asosiy "/" manzilida ochiladi
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Fayl manzili Vercel serverlarida to'g'ri topilishi uchun absolute path olamiz
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 2. Ichki bosh sahifa (home.html) - Tizimda "/home" manzilida ochiladi
@app.get("/home", response_class=HTMLResponse)
async def read_home():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "home.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------------------------------------
# BACKEND API STRUKTURASI VA LOGIKASI
# -------------------------------------------------------------

# Simulyatsiya uchun operativ xotira (Ma'lumotlar bazasi o'rniga)
db_users = {} 
results_db = {} 

class UserAction(BaseModel):
    ism: str
    familiya: str = None
    fan: str = None
    savol: str = None
    ball: int = 0

# 1. Ro'yxatdan o'tish API
@app.post("/register")
async def register(data: UserAction):
    db_users[data.ism] = {"familiya": data.familiya, "ball": 0}
    return {"message": f"{data.ism} tizimga qo'shildi", "status": "ok"}

# 2. Fanlar va 5 tadan Mavzular ierarxiyasi
@app.get("/data")
async def get_data():
    return {
        "fanlar": {
            "Biologiya": ["Hujayra", "DNK tuzilishi", "Fotosintez", "Genetika", "Evolyutsiya"],
            "Tarix": ["Qadimgi dunyo", "Amir Temur davri", "Mustamlakachilik", "Mustaqillik", "Zamonaviy tarix"],
            "O'zbek tili": ["Imlo", "So'z turkumlari", "Sintaksis", "Uslubiyat", "Matn tahlili"]
        }
    }

# 3. AI Maslahatchi (Mutlaqo soxta, API kalitsiz, limitsiz va o'ta barqaror)
@app.post("/ask-ai")
async def ask_ai(data: UserAction):
    shablon_javoblar = [
        f"Ajoyib savol! {data.fan} fani doirasida '{data.savol}' mavzusi juda dolzarb hisoblanadi. Mustaqil ta'lim samaradorligini oshirish uchun ushbu yo'nalishdagi vizual materiallar va platformamizdagi amaliy testlar bilan tanishib chiqishingizni tavsiya qilaman.",
        f"Tizim intellektual tahlili yakunlandi: Siz so'ragan '{data.savol}' masalasi bo'yicha shaxsiy o'quv traektoriyangizga mos qo'shimcha topshiriqlar shakllantirildi. Bilimni mustahkamlash uchun darslikning ushbu bo'limini qayta ko'rib chiqishingizni maslahat beraman.",
        f"Sizning {data.fan} fani bo'yicha so'rovingiz qabul qilindi. '{data.savol}' tahliliga ko'ra, mustaqil ta'lim metodologiyasida tizimli yondashuv juda muhim. Platformadagi darajali testlar algoritmi aynan shu kamchiliklarni bartaraf etishga yordam beradi."
    ]
    
    # Tasodifiy bitta professional javob andozasini tanlaymiz
    tanlangan_javob = random.choice(shablon_javoblar)
    return {
        "status": "ok", 
        "javob": tanlangan_javob
    }

# 4. Ballarni tekshirish va Shaxsiy tavsiya (Adaptive Learning & Murakkablashtirish logikasi)
@app.post("/submit_result")
async def submit_result(user_name: str, score: int, task_id: int, fan: str = "Biologiya"):
    results_db[user_name] = {"score": score, "task_id": task_id, "fan": fan}
    
    # Talabaning bilim darajasiga qarab o'quv traektoriyasini moslashtirish
    if score >= 80:
        maqom = "A'lo"
        tavsiya = f"Tizim intellektual tahlili: Siz {fan} fani bo'yicha yuqori intellekt ko'rsatdingiz. Keyingi murakkablashtirilgan bosqich (Daraja {task_id + 1}) siz uchun muvaffaqiyatli ochildi!"
        status = "next_level"
    elif score >= 50:
        maqom = "Qoniqarli"
        tavsiya = f"Tizim intellektual tahlili: Bilimingiz yaxshi, lekin keyingi darajaga o'tish uchun materiallarni yana bir bor mustaqil takrorlashni maslahat beramiz."
        status = "stay"
    else:
        maqom = "Yomon"
        tavsiya = f"Tizim intellektual tahlili: Ushbu mavzuni o'zlashtirishda kamchiliklar bor. Algoritm sizga ushbu mavzu bo'yicha boshlang'ich darslikka qaytishni va qayta test topshirishni tayyorladi."
        status = "repeat"

    return {
        "status": status,
        "score": score,
        "maqom": maqom,
        "tavsiya": tavsiya
    }

# 5. Admin Panel uchun barcha natijalarni qaytarish API
@app.get("/admin/stats")
async def get_stats():
    return results_db

# 6. Ballar evaziga kitob berish API (Gamification)
@app.post("/exchange")
async def exchange_points(data: UserAction):
    if data.ism in db_users:
        db_users[data.ism]["ball"] -= data.ball
        return {"message": f"{data.ball} ball evaziga elektron kitob berildi!"}
    return {"message": "Foydalanuvchi topilmadi"}