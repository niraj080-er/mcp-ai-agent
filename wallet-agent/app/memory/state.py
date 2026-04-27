from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WalletAgentState(BaseModel):
    thread_id: str

    programManagerId: Optional[str] = None
    walletId: Optional[str] = None
    personId: Optional[str] = None
    mobileNumber: Optional[str] = None
    cifNumber: Optional[str] = None
    transactionId: Optional[str] = None
    tagId: Optional[str] = None
    transferTypeId: Optional[str] = None
    groupId: Optional[str] = None
    customFieldId: Optional[str] = None
    customFieldValue: Optional[str] = None

    pending_tool_name: Optional[str] = None
    pending_backend_tool_name: Optional[str] = None
    pending_arguments: Dict[str, Any] = Field(default_factory=dict)
    pending_missing_fields: List[str] = Field(default_factory=list)

    last_tool_name: Optional[str] = None
    last_tool_result_summary: Dict[str, Any] = Field(default_factory=dict)
    recent_messages: List[Dict[str, str]] = Field(default_factory=list)
    conversation_summary: Optional[str] = None