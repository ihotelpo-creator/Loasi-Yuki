"""
LINE MCP Client Integration Module
Demonstrates standard Model Context Protocol (MCP) usage with LINE Bot MCP Server.
"""

import os
import logging
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger("LineMCP")

class LineMCPClient:
    """
    Client wrapper to interact with line-bot-mcp-server endpoints.
    Allows AI Agents (Claude, Gemini, Antigravity) to send Flex Messages,
    retrieve user profiles, and manage LINE OA via MCP standard tools.
    """
    def __init__(self, mcp_server_url: str = "http://localhost:3000"):
        self.mcp_server_url = mcp_server_url
        self.channel_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Calls a tool on the LINE MCP Server."""
        url = f"{self.mcp_server_url}/tools/{tool_name}/invoke"
        headers = {
            "Authorization": f"Bearer {self.channel_token}",
            "Content-Type": "application/json"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json={"arguments": arguments}, headers=headers)
                return response.json()
        except Exception as e:
            logger.error(f"Failed to invoke MCP tool '{tool_name}': {e}")
            return {"status": "error", "message": str(e)}

    async def send_flashcard_via_mcp(self, user_id: str, flashcard_data: dict) -> dict:
        """Example tool call: Send Flex Message via LINE MCP Tool."""
        return await self.call_tool(
            tool_name="send_flex_message",
            arguments={
                "to": user_id,
                "altText": f"คำศัพท์ภาษาจีน: {flashcard_data.get('word_cn')}",
                "contents": flashcard_data
            }
        )
