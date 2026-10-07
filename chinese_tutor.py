"""
Chinese Tutor AI Core Logic powered by Google Gemini API
"""

import os
import json
import logging
from typing import Dict, Any, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger("ChineseTutor")

class ChineseTutorEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key and genai:
            genai.configure(api_key=self.api_key)

    def _generate(self, prompt: str) -> str:
        """Helper to try generating content with fallback Gemini models."""
        if not self.api_key or not genai:
            raise ValueError("GEMINI_API_KEY is missing or genai package is unavailable")

        candidate_models = [
            'gemini-3.8-flash',
            'gemini-3.6-flash',
            'gemini-flash-latest',
            'gemini-2.5-flash-lite',
            'gemini-pro-latest'
        ]

        last_exception = None
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                last_exception = e
                logger.warning("Gemini model %s failed: %s", model_name, e)

        raise RuntimeError(f"All Gemini models failed. Last error: {last_exception}")

    def chat_response(self, user_message: str, user_id: str = "default") -> str:
        """Processes regular chat / roleplay with the student."""
        if not self.api_key:
            return f"🇨🇳 [โหมดจำลอง (No API Key)] คุณพูดว่า: '{user_message}'\n\nพินอิน: [nǐ hǎo]\nแปลไทย: สวัสดีครับ! กรุณาใส่ GEMINI_API_KEY เพื่อเปิดใช้งาน AI เต็มรูปแบบ"

        prompt = f"""
        คุณคือ 'ครูสอนภาษาจีน AI' ที่ใจดี กระตือรือร้น และเป็นกันเอง
        หน้าที่ของคุณคือสนทนาภาษาจีนกับผู้เรียนชาวไทย
        
        กฎการตอบ:
        1. ตอบโต้เป็นภาษาจีนง่ายๆ (ระดับ HSK 1-4)
        2. ทุกประโยคภาษาจีน **ต้องกำกับพินอิน (Pinyin)**
        3. แปลความหมายเป็นภาษาไทยสั้นๆ
        4. หากข้อความของผู้เรียนมีคำผิดทางไวยากรณ์ ให้ช่วยแก้ไขและบอกประโยคที่ถูกอย่างสุภาพ
        
        ข้อความของผู้เรียน: {user_message}
        """
        try:
            return self._generate(prompt)
        except Exception as e:
            err_str = str(e)
            logger.error("Gemini API error: %s", err_str)
            if "429" in err_str or "quota" in err_str.lower():
                return "⚠️ โควต้าการใช้งาน Gemini API ฟรีของวันนี้เต็มชั่วคราวครับ (Google Quota Limit)\n\n💡 วิธีแก้ไข: กรุณาสร้าง Gemini API Key ใหม่ฟรีที่ aistudio.google.com แล้วนำไปอัปเดตใน Render.com ครับ"
            return f"ขออภัยครับ เกิดข้อผิดพลาดในการประมวลผล AI: {err_str[:150]}"

    def generate_flashcard(self, hsk_level: str = "HSK 1") -> Dict[str, Any]:
        """Generates a structured HSK vocabulary item in JSON format."""
        default_card = {
            "word_cn": "朋友",
            "pinyin": "péng you",
            "thai_meaning": "เพื่อน",
            "example_cn": "他是我的好朋友。",
            "example_th": "เขาเป็นเพื่อนที่ดีของฉัน",
            "hsk_level": hsk_level
        }
        if not self.api_key:
            return default_card

        prompt = f"""
        สุ่มสร้างคำศัพท์ภาษาจีนระดับ {hsk_level} มา 1 คำ 
        ส่งคืนคำตอบในรูปแบบ JSON สตริงแบบแท้จริง (JSON only) ดังนี้:
        {{
            "word_cn": "คำศัพท์จีน",
            "pinyin": "pinyin",
            "thai_meaning": "แปลไทย",
            "example_cn": "ประโยคตัวอย่างจีน",
            "example_th": "แปลประโยคตัวอย่างไทย",
            "hsk_level": "{hsk_level}"
        }}
        """
        try:
            raw_text = self._generate(prompt)
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.error("Error generating flashcard: %s", e)
            return default_card

    def check_grammar(self, sentence: str) -> Dict[str, Any]:
        """Checks and corrects a Chinese sentence written by the user."""
        if not self.api_key:
            return {
                "original_text": sentence,
                "corrected_text": sentence,
                "pinyin": "Nǐ hǎo",
                "explanation_th": "ระบบจำลองการตรวจไวยากรณ์ (ใส่ API Key เพื่อใช้งานจริง)"
            }

        prompt = f"""
        โปรดตรวจไวยากรณ์ประโยคภาษาจีนนี้: "{sentence}"
        ส่งคืนคำตอบเป็น JSON รูปแบบนี้เท่านั้น:
        {{
            "original_text": "{sentence}",
            "corrected_text": "ประโยคที่ถูกต้อง",
            "pinyin": "pinyin ของประโยคที่ถูกต้อง",
            "explanation_th": "อธิบายจุดผิดหรือข้อแนะนำเป็นภาษาไทย"
        }}
        """
        try:
            raw_text = self._generate(prompt)
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.error("Error checking grammar: %s", e)
            return {
                "original_text": sentence,
                "corrected_text": sentence,
                "pinyin": "",
                "explanation_th": f"ไม่สามารถตรวจไวยากรณ์ได้ชั่วคราว (Quota API เต็ม) กรุณาเปลี่ยน Gemini API Key"
            }
