# Poke MCP Server

An MCP server that wraps the [Poke](https://poke.com) AI assistant API, so you can use Poke from Claude Code, Claude Desktop (Cowork), and Claude chat.

## Prerequisites

1. A Poke account with API access
2. An API key from [poke.com/settings/advanced](https://poke.com/settings/advanced)

## Quick Start (Local / Claude Code)

```bash
git clone https://github.com/bort911/poke-mcp-server.git
cd poke-mcp-server
pip install -r requirements.txt
export POKE_API_KEY="your-api-key-here"
python src/server.py --stdio
```

## Deploy to Render (for Cowork / Claude Chat)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bort911/poke-mcp-server)

1. Click the button above
2. Set the `POKE_API_KEY` environment variable in Render
3. Your server will be at `https://your-service.onrender.com/mcp`

## Claude Code Configuration

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "poke": {
      "command": "python",
      "args": ["/path/to/poke-mcp-server/src/server.py", "--stdio"],
      "env": {
        "POKE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tools

- **poke_send_message** - Send a message to Poke and get a response
- **poke_server_info** - Check server status and API key configuration
