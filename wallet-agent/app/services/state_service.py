from __future__ import annotations

from typing import Dict, Any, List

from app.memory.state import WalletAgentState


class StateService:
    def __init__(self) -> None:
        self._store: Dict[str, WalletAgentState] = {}

    def get_or_create(self, thread_id: str) -> WalletAgentState:
        if thread_id not in self._store:
            self._store[thread_id] = WalletAgentState(thread_id=thread_id)
        return self._store[thread_id]

    def save(self, state: WalletAgentState) -> None:
        self._store[state.thread_id] = state

    def set_pending_tool(
        self,
        state: WalletAgentState,
        tool_name: str,
        backend_tool_name: str,
        arguments: Dict[str, Any],
        missing_fields: List[str],
    ) -> None:
        state.pending_tool_name = tool_name
        state.pending_backend_tool_name = backend_tool_name
        state.pending_arguments = arguments or {}
        state.pending_missing_fields = missing_fields or []
        self.save(state)

    def clear_pending_tool(self, state: WalletAgentState) -> None:
        state.pending_tool_name = None
        state.pending_backend_tool_name = None
        state.pending_arguments = {}
        state.pending_missing_fields = []
        self.save(state)