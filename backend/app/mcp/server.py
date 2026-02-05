"""
MCP (Model Context Protocol) Server.

This module implements the official MCP SDK server and registers the 5 todo tools.
"""
from typing import Dict, Any
import asyncio
from mcp.server import Server
from mcp.types import CallToolResult
from .tools import MCP_TOOLS


class MCPServer:
    def __init__(self):
        self.server = Server("todo-mcp-server", "1.0.0")
        self.register_tools()

    def register_tools(self):
        """Register all 5 todo tools with the MCP server."""
        for tool_name, tool_info in MCP_TOOLS.items():
            # Register each tool with the MCP server
            @self.server.tool(
                name=tool_name,
                description=tool_info["description"],
                input_schema=tool_info["parameters"]
            )
            async def tool_handler(tool_name=tool_name, arguments: Dict[str, Any] = {}) -> CallToolResult:
                # Get the actual function for this tool
                tool_func = MCP_TOOLS[tool_name]["function"]

                # Call the tool function with the provided arguments
                try:
                    # The arguments should be converted to the expected input format
                    # In practice, this would involve mapping the arguments properly
                    result = tool_func(arguments)

                    return CallToolResult(content=[
                        {
                            "type": "text",
                            "text": str(result)
                        }
                    ])
                except Exception as e:
                    return CallToolResult(
                        content=[
                            {
                                "type": "text",
                                "text": f"Error executing {tool_name}: {str(e)}"
                            }
                        ],
                        isError=True
                    )

    async def serve(self, host: str = "127.0.0.1", port: int = 3000):
        """Start the MCP server."""
        print(f"MCP Server starting on {host}:{port}")
        await self.server.serve()


# Global server instance
mcp_server = MCPServer()


async def run_mcp_server():
    """Convenience function to run the MCP server."""
    await mcp_server.serve()