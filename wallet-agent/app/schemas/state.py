from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class StateResponse(BaseModel):
    thread_id: str
    current_domain: Optional[str] = None
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
    last_tool_name: Optional[str] = None
    last_tool_result_summary: Dict[str, Any] = {}
    conversation_summary: Optional[str] = None