"""
FastAPI Server for LINE AI Chinese Tutor Bot & LINE MCP Server Integration
"""

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Header, BackgroundTasks
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from chinese_tutor import ChineseTutorEngine
from flex_templates import create_flashcard_flex, create_grammar_correction_flex, create_menu_flex

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LineBot")

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "MOCK_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "MOCK_SECRET")

app = FastAPI(
    title="LINE AI Chinese Tutor Bot",
    description="A Chinese Learning & Practice Chatbot for LINE platform powered by AI & LINE MCP",
    version="1.0.0"
)

# LINE Bot SDK initialization
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# AI Tutor Engine
tutor = ChineseTutorEngine()


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "LINE AI Chinese Tutor Bot",
        "mcp_enabled": True
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request, x_line_signature: str = Header(None)):
    """LINE Webhook endpoint."""
    body = await request.body()
    body_str = body.decode('utf-8')
    logger.info("Received Webhook event: %s", body_str)

    if LINE_CHANNEL_SECRET == "MOCK_SECRET":
        logger.info("Received Webhook payload (MOCK MODE): %s", body_str[:200])
        return {"status": "success", "note": "Mock mode active"}

    if not x_line_signature:
        logger.warning("Missing X-Line-Signature header")
        return {"status": "ok", "message": "Missing X-Line-Signature header"}

    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        logger.error("Invalid LINE signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error("Error processing webhook: %s", e, exc_info=True)
        return {"status": "error", "message": str(e)}

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_text = event.message.text.strip()
    reply_token = event.reply_token

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 1. Main Menu Command
        if user_text.lower() in ["เมนู", "menu", "เริ่มต้น", "help"]:
            menu_flex = create_menu_flex()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[
                        FlexMessage(altText="🇨🇳 AI Chinese Tutor Menu", contents=FlexContainer.from_dict(menu_flex))
                    ]
                )
            )
            return

        # 2. Vocabulary Flashcard Command
        if "ขอคำศัพท์" in user_text or "คำศัพท์" in user_text:
            card_data = tutor.generate_flashcard("HSK 1")
            flash_flex = create_flashcard_flex(**card_data)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[
                        FlexMessage(altText=f"คำศัพท์: {card_data['word_cn']}", contents=FlexContainer.from_dict(flash_flex))
                    ]
                )
            )
            return

        # 3. Sentence Practice / Grammar Check Command
        if user_text.startswith("ฝึกแต่งประโยค") or user_text.startswith("ตรวจประโยค"):
            sentence = user_text.replace("ฝึกแต่งประโยคคำว่า", "").replace("ฝึกแต่งประโยค", "").replace("ตรวจประโยค", "").strip()
            if not sentence:
                sentence = "你好"
            grammar_res = tutor.check_grammar(sentence)
            grammar_flex = create_grammar_correction_flex(**grammar_res)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[
                        FlexMessage(altText="ผลการตรวจไวยากรณ์", contents=FlexContainer.from_dict(grammar_flex))
                    ]
                )
            )
            return

        # 4. Roleplay & Conversation Mode (Default LLM Answer)
        reply_text = tutor.chat_response(user_text, user_id=event.source.user_id)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=True)
