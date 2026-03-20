#!/usr/bin/env python3
"""
Poke MCP Server - Wraps the Poke AI assistant API so you can use it
from Claude Code, Cowork, and Claude chat via MCP.
"""
import os
import httpx
from fastmcp import FastMCP

POKE_API_URL = "https://poke.com/api/v1/inbound-sms/webhook"

mcp = FastMCP("poke_mcp")


def _get_api_key() -> str:
    """Get the Poke API key from environment."""
    key = os.environ.get("POKE_API_KEY")
    if not key:
        raise ValueError(
            "POKE_API_KEY environment variable is not set. "
            "Get your API key at https://poke.com/settings/advanced"
        )
    return key


@mcp.tool(
    name="poke_send_message",
    description=(
        "Send a message to Poke, your AI assistant that lives in iMessage. "
        "Use this to delegate tasks to Poke, ask it questions, or trigger "
        "any integrations you have connected in Poke. "
        "Returns Poke's response."
    ),
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def poke_send_message(message: str) -> str:
    """Send a message to Poke and return the response.

    Args:
        message: The message to send to Poke. Can be a question,
                 task, or command for any of your Poke integrations.
    """
    api_key = _get_api_key()

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            POKE_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"message": message},
        )

        if response.status_code == 401:
            return (
                "Authentication failed. Check your POKE_API_KEY. "
                "You can get/regenerate your key at https://poke.com/settings/advanced"
            )
        elif response.status_code == 429:
            return "Rate limited by Poke API. Wait a moment and try again."
        elif response.status_code >= 400:
            return f"Poke API error (HTTP {response.status_code}): {response.text}"

        try:
            data = response.json()
            if isinstance(data, dict):
                return data.get("response", data.get("message", str(data)))
            return str(data)
        except Exception:
            return response.text


@mcp.tool(
    name="poke_server_info",
    description="Get info about this Poke MCP server and connection status.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def poke_server_info() -> dict:
    """Check the server status and whether the API key is configured."""
    has_key = bool(os.environ.get("POKE_API_KEY"))
    return {
        "server": "poke_mcp",
        "version": "1.0.0",
        "api_key_configured": has_key,
        "poke_settings_url": "https://poke.com/settings/advanced",
        "poke_integrations_url": "https://poke.com/settings/connections",
    }


if __name__ == "__main__":
    import sys

    if "--stdio" in sys.argv:
        mcp.run(transport="stdio")
    else:
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        print(f"Starting Poke MCP server on {host}:{port}")
        mcp.run(
            transport="http",
            host=host,
            port=port,
            stateless_http=True,
        )
