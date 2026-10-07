# 🇨🇳 LINE AI Chinese Tutor Bot (with LINE MCP Support)

ระบบ **LINE Bot สนทนาและสอนภาษาจีนด้วย AI** ที่มาพร้อมกับการรองรับ **LINE MCP (Model Context Protocol)** และ **LINE Messaging API**

---

## 🌟 ฟีเจอร์หลัก (Features)

1. **🗣️ AI Roleplay & Conversation (สนทนาโต้ตอบแบบธรรมชาติ):**
   * สนทนาภาษาจีนระดับ HSK 1-4
   * มี **พินอิน (Pinyin)** กำกับทุกประโยคพร้อมคำแปลภาษาไทย
2. **📚 HSK Flashcards (การ์ดคำศัพท์ Flex Message):**
   * ส่งการ์ดคำศัพท์ภาษาจีนแบบ Flex Message สวยงาม
   * แสดงตัวอย่างประโยค และปุ่มโต้ตอบขอศัพท์ถัดไป / ฝึกแต่งประโยค
3. **✨ Grammar & Pinyin Checker (ตรวจไวยากรณ์ภาษาจีน):**
   * ตรวจประโยคภาษาจีนที่ผู้เรียนพิมพ์ พร้อมแสดงประโยคก่อน-หลังแก้ไข และอธิบายจุดผิด
4. **🔌 LINE MCP Ready:**
   * ออกแบบโครงสร้างรองรับการเชื่อมต่อกับ `line-bot-mcp-server` เพื่อสั่งการผ่าน AI Agents (Claude / Gemini Agent)

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```
line-chinese-bot/
├── app.py                # FastAPI Server สำหรับรับ Webhook จาก LINE
├── chinese_tutor.py      # ตัวประมวลผล AI Tutor ด้วย Gemini API
├── flex_templates.py     # เทมเพลต LINE Flex Message (คำศัพท์, ไวยากรณ์, เมนู)
├── mcp_client.py         # ตัวเชื่อมต่อกับ LINE MCP Server
├── requirements.txt      # รายการ Python dependencies
└── .env.example          # ตัวอย่างไฟล์ตั้งค่าคอนฟิก
```

---

## 🛠️ วิธีการติดตั้งและใช้งาน (Setup & Usage)

### 1. สร้าง Virtual Environment และติดตั้ง Packages

```bash
cd /Users/petch.mac/.gemini/antigravity/scratch/line-chinese-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. ตั้งค่าไฟล์ `.env`

คัดลอกไฟล์ `.env.example` เป็น `.env` แล้วระบุข้อมูล:

```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env`:
```env
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_CHANNEL_SECRET=your_channel_secret
GEMINI_API_KEY=your_gemini_api_key
```

### 3. รันเซิร์ฟเวอร์ (FastAPI)

```bash
python3 app.py
# หรือใช้ uvicorn
uvicorn app:app --reload --port 8000
```

---

## 🔗 การตั้งค่า Webhook บน LINE Developers Console

1. ไปที่ [LINE Developers Console](https://developers.line.biz/)
2. สร้าง Channel ชนิด **Messaging API**
3. คัดลอก **Channel Access Token** และ **Channel Secret** นำไปใส่ในไฟล์ `.env`
4. เปิดใช้งาน **ngrok** เพื่อส่ง Webhook เข้าพอร์ต 8000 บนเครื่องของคุณ:
   ```bash
   ngrok http 8000
   ```
5. นำ URL ที่ได้จาก ngrok (เช่น `https://xxxx.ngrok-free.app/webhook`) ไปวางในช่อง **Webhook URL** บน LINE Developers Console และกดเปิด **Use webhook**

---

## 🤖 การเชื่อมต่อกับ LINE MCP Server

โปรเจกต์นี้มี `mcp_client.py` สำหรับเชื่อมต่อกับ [line-bot-mcp-server](https://github.com/line/line-bot-mcp-server) เพื่อให้ AI Agent สามารถเรียกใช้เครื่องมือส่งคำศัพท์ หรือจัดการ Rich Menu ได้โดยตรงแบบมาตรฐาน MCP!
