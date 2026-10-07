"""
LINE Flex Message Templates for Chinese Learning Bot
"""

def create_flashcard_flex(word_cn: str, pinyin: str, thai_meaning: str, example_cn: str, example_th: str, hsk_level: str = "HSK 1") -> dict:
    """Generates an HSK vocabulary flashcard Flex Message."""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#1DB446",
            "contents": [
                {
                    "type": "text",
                    "text": f"📚 การ์ดคำศัพท์ประจำวัน ({hsk_level})",
                    "color": "#FFFFFF",
                    "weight": "bold",
                    "size": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": word_cn,
                    "weight": "bold",
                    "size": "5xl",
                    "align": "center",
                    "color": "#1E293B",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"[{pinyin}]",
                    "align": "center",
                    "color": "#0284C7",
                    "size": "lg",
                    "weight": "bold",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"💡 ความหมาย: {thai_meaning}",
                            "size": "md",
                            "color": "#334155",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"🇨🇳 ตัวอย่าง: {example_cn}",
                            "size": "sm",
                            "color": "#475569",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": f"🇹🇭 แปล: {example_th}",
                            "size": "sm",
                            "color": "#64748B",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "คำศัพท์ถัดไป ➡️",
                        "text": "ขอคำศัพท์"
                    },
                    "style": "primary",
                    "color": "#1DB446"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "ฝึกแต่งประโยค ✍️",
                        "text": f"ฝึกแต่งประโยคคำว่า {word_cn}"
                    },
                    "style": "secondary"
                }
            ]
        }
    }


def create_grammar_correction_flex(original_text: str, corrected_text: str, pinyin: str, explanation_th: str) -> dict:
    """Generates a Grammar Correction Flex Message."""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#0EA5E9",
            "contents": [
                {
                    "type": "text",
                    "text": "✨ ตรวจไวยากรณ์ภาษาจีน (Grammar Check)",
                    "color": "#FFFFFF",
                    "weight": "bold",
                    "size": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FEF2F2",
                    "paddingAll": "md",
                    "cornerRadius": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "❌ ประโยคเดิม:",
                            "size": "xs",
                            "color": "#991B1B",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": original_text,
                            "size": "md",
                            "color": "#7F1D1D",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F0FDF4",
                    "paddingAll": "md",
                    "cornerRadius": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "✅ ประโยคที่ถูกต้อง:",
                            "size": "xs",
                            "color": "#166534",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": corrected_text,
                            "size": "md",
                            "color": "#14532D",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": f"[{pinyin}]",
                            "size": "xs",
                            "color": "#0284C7",
                            "margin": "xs"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💡 คำอธิบาย:",
                            "size": "xs",
                            "color": "#475569",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": explanation_th,
                            "size": "sm",
                            "color": "#334155",
                            "wrap": True
                        }
                    ]
                }
            ]
        }
    }


def create_menu_flex() -> dict:
    """Generates the Main Interactive Menu Flex Message."""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#4F46E5",
            "contents": [
                {
                    "type": "text",
                    "text": "🇨🇳 AI Chinese Tutor Menu",
                    "color": "#FFFFFF",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "เลือกโหมดที่ต้องการฝึกฝนได้เลยครับ",
                    "color": "#E0E7FF",
                    "size": "xs"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "🗣️ ซ้อมสนทนา (Roleplay)",
                        "text": "เริ่มโหมดสนทนา"
                    },
                    "style": "primary",
                    "color": "#4F46E5"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "📚 คำศัพท์ HSK ประจำวัน",
                        "text": "ขอคำศัพท์"
                    },
                    "style": "secondary"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "📝 ทดสอบความรู้ (Quiz)",
                        "text": "เริ่มทำควิซ"
                    },
                    "style": "secondary"
                }
            ]
        }
    }
