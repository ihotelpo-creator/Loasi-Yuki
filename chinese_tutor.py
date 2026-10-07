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
            logger.error("Gemini API error: %s", e)
            return f"ขออภัยครับ เกิดข้อผิดพลาดในการประมวลผล AI: {str(e)}"

    def generate_flashcard(self, hsk_level: str = "HSK 1") -> Dict[str, Any]:
        """Generates a structured HSK vocabulary item in JSON format."""
        if not self.api_key:
            return {
                "word_cn": "学习",
                "pinyin": "xué xí",
                "thai_meaning": "เรียน / เรียนรู้",
                "example_cn": "我喜欢学习中文。",
                "example_th": "ฉันชอบเรียนภาษาจีน",
                "hsk_level": hsk_level
            }

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
            return {
                "word_cn": "苹果",
                "pinyin": "píng guǒ",
                "thai_meaning": "แอปเปิ้ล",
                "example_cn": "我吃苹果。",
                "example_th": "ฉันกินแอปเปิ้ล",
                "hsk_level": hsk_level
            }

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
                "explanation_th": f"ไม่สามารถตรวจไวยากรณ์ได้: {str(e)}"
            }
