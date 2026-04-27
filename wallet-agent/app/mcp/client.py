from __future__ import annotations

import httpx

from app.core.config import get_settings, load_yaml_config
from app.core.logging import get_logger
from app.core.exceptions import ConfigurationError

logger = get_logger(__name__)


class MCPHttpClient:
    def __init__(self) -> None:
        settings = get_settings()
        cfg = load_yaml_config()["mcp"]

        self.url = cfg["url"].strip()
        self.timeout = 30.0
        self.token = (settings.mcp_bearer_token or "").strip()

        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        logger.info("Initialized MCP client with url=%s", self.url)

    def _headers_for_tools_list(self) -> dict:
        return dict(self.base_headers)

    def _headers_for_tool_call(self) -> dict:
        if not self.token:
            raise ConfigurationError("MCP_BEARER_TOKEN is required for tools/call")

        headers = dict(self.base_headers)
        headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _post_rpc(self, payload: dict, headers: dict) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.url, json=payload, headers=headers)

            safe_headers = {
                k: ("Bearer ***" if k.lower() == "authorization" else v)
                for k, v in headers.items()
            }

            if response.status_code >= 400:
                logger.error(
                    "MCP request failed | url=%s | status=%s | payload=%s | headers=%s | response=%s",
                    self.url,
                    response.status_code,
                    payload,
                    safe_headers,
                    response.text,
                )
                response.raise_for_status()

            logger.info(
                "MCP request success | method=%s | headers=%s",
                payload.get("method"),
                safe_headers,
            )

            return response.json()

    async def tools_list(self) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        }
        return await self._post_rpc(payload, self._headers_for_tools_list())

    async def tool_call(self, name: str, arguments: dict) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            },
        }
        return await self._post_rpc(payload, self._headers_for_tool_call())


def get_mcp_client() -> MCPHttpClient:
    return MCPHttpClient()