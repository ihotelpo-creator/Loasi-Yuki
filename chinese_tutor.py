"""
Chinese Tutor AI Core Logic powered by Google Gemini API
Optimized for low-token usage and API Key rotation.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger("ChineseTutor")

class ChineseTutorEngine:
    def __init__(self, api_key_str: Optional[str] = None):
        raw_keys = api_key_str or os.getenv("GEMINI_API_KEY", "")
        # Support multiple API keys separated by comma or whitespace
        self.api_keys: List[str] = [k.strip() for k in raw_keys.replace(",", " ").split() if k.strip()]
        self.current_key_index = 0

    def _get_active_api_key(self) -> Optional[str]:
        if not self.api_keys:
            return None
        return self.api_keys[self.current_key_index % len(self.api_keys)]

    def _rotate_key(self):
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            logger.info("Rotated to next Gemini API Key (Index: %d)", self.current_key_index)

    def _generate(self, prompt: str) -> str:
        """Helper to generate content with lightweight models and API key rotation."""
        if not self.api_keys or not genai:
            raise ValueError("GEMINI_API_KEY is missing or genai package is unavailable")

        # Lightweight models first for maximum speed and lowest token quota usage
        candidate_models = [
            'gemini-2.5-flash-lite',
            'gemini-3.5-flash-lite',
            'gemini-3.8-flash',
            'gemini-3.6-flash',
            'gemini-flash-latest'
        ]

        # Try across active keys and models
        key_attempts = len(self.api_keys)
        last_exception = None

        for _ in range(key_attempts):
            active_key = self._get_active_api_key()
            genai.configure(api_key=active_key)

            for model_name in candidate_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text.strip()
                except Exception as e:
                    last_exception = e
                    err_str = str(e)
                    logger.warning("Model %s failed with key index %d: %s", model_name, self.current_key_index, err_str)
                    if "429" in err_str or "quota" in err_str.lower():
                        # Key reached quota limit -> try next key
                        break

            # Rotate to next key if available
            self._rotate_key()

        raise RuntimeError(f"All Gemini models & keys failed. Last error: {last_exception}")

    def chat_response(self, user_message: str, user_id: str = "default") -> str:
        """Processes regular chat / roleplay with concise, token-optimized answers."""
        if not self.api_keys:
            return f"🇨🇳 [โหมดจำลอง (No API Key)] คุณพูดว่า: '{user_message}'\n\nพินอิน: [nǐ hǎo]\nแปลไทย: สวัสดีครับ! กรุณาใส่ GEMINI_API_KEY เพื่อเปิดใช้งาน AI เต็มรูปแบบ"

        prompt = f"""
        คุณคือ 'ครูสอนภาษาจีน AI' ที่ตอบสั้น กระชับ ตรงประเด็น
        
        กฎการตอบ:
        1. ตอบไม่เกิน 2-3 ประโยค
        2. ภาษาจีนสั้นๆ (HSK 1-4)
        3. มีพินอิน (Pinyin) กำกับทุกประโยคจีน
        4. แปลไทยสั้นกระชับ (ห้ามเกริ่นยาว)
        5. หากผู้เรียนพิมพ์ผิด ให้แก้ไวยากรณ์สั้นๆ
        
        ข้อความของผู้เรียน: {user_message}
        """
        try:
            return self._generate(prompt)
        except Exception as e:
            err_str = str(e)
            logger.error("Gemini API error: %s", err_str)
            if "429" in err_str or "quota" in err_str.lower():
                return "⚠️ โควต้า Gemini API ของวันนี้เต็มชั่วคราวครับ (Quota Exceeded)\n\n💡 แนะนำ: ใส่ API Key สำรองเพิ่มใน Render.com หรือรอการรีเซ็ตฟรีประจำวันครับ"
            return f"ขออภัยครับ เกิดข้อผิดพลาดในการประมวลผล AI: {err_str[:150]}"

    def generate_flashcard(self, hsk_level: str = "HSK 1") -> Dict[str, Any]:
        """Generates a concise structured HSK vocabulary flashcard."""
        default_card = {
            "word_cn": "朋友",
            "pinyin": "péng you",
            "thai_meaning": "เพื่อน",
            "example_cn": "他是我的好朋友。",
            "example_th": "เขาเป็นเพื่อนที่ดีของฉัน",
            "hsk_level": hsk_level
        }
        if not self.api_keys:
            return default_card

        prompt = f"""
        สุ่มสร้างคำศัพท์ภาษาจีน {hsk_level} มา 1 คำ และประโยคตัวอย่างสั้นๆ
        ตอบเป็น JSON สตริงแท้จริง (JSON only, no markdown):
        {{
            "word_cn": "คำศัพท์จีน",
            "pinyin": "pinyin",
            "thai_meaning": "แปลไทยสั้นๆ",
            "example_cn": "ประโยคสั้น",
            "example_th": "แปลประโยคสั้น",
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
        """Checks and corrects Chinese grammar concisely."""
        if not self.api_keys:
            return {
                "original_text": sentence,
                "corrected_text": sentence,
                "pinyin": "Nǐ hǎo",
                "explanation_th": "ระบบจำลองการตรวจไวยากรณ์ (ใส่ API Key เพื่อใช้งานจริง)"
            }

        prompt = f"""
        ตรวจไวยากรณ์ประโยคภาษาจีนนี้: "{sentence}"
        ตอบเป็น JSON สตริงแท้จริง (JSON only, no markdown):
        {{
            "original_text": "{sentence}",
            "corrected_text": "ประโยคที่ถูก",
            "pinyin": "pinyin ประโยคที่ถูก",
            "explanation_th": "อธิบายสั้นๆ ไม่เกิน 1-2 บรรทัด"
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
                "explanation_th": f"ไม่สามารถตรวจไวยากรณ์ได้ชั่วคราว (Quota API เต็ม)"
            }
