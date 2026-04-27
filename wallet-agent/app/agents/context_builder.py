from __future__ import annotations

from app.memory.state import WalletAgentState


def build_context_block(state: WalletAgentState) -> str:
    return f"""
Structured session context:
- programManagerId: {state.programManagerId}
- walletId: {state.walletId}
- personId: {state.personId}
- mobileNumber: {state.mobileNumber}
- cifNumber: {state.cifNumber}
- transactionId: {state.transactionId}
- tagId: {state.tagId}
- transferTypeId: {state.transferTypeId}
- groupId: {state.groupId}
- customFieldId: {state.customFieldId}
- customFieldValue: {state.customFieldValue}
- last_tool_name: {state.last_tool_name}
- last_tool_result_summary: {state.last_tool_result_summary}
- conversation_summary: {state.conversation_summary}

Instructions:
- Use the above context to select the best tool for the user's request.
- If multiple tools are relevant, select the one that best matches the user's intent.
- If no tools are relevant, return null for the tool name.
- Do not attempt to fill in missing fields or guess values.
- If business identity fields are missing, you can still select a tool if the available information strongly
- indicates that the tool is relevant. Do not reject tools solely due to missing business identity fields.
- The application will ask the user for any missing business identity fields after tool selection if needed.
- Always use the provided catalog of tools and do not attempt to use any tools outside of that catalog.
- Use the session context to understand follow-up phrases such as “that wallet”, “same person”, “same mobile number”, or “that transaction”.
- Reuse saved identifiers only when they are clearly present in the session context.
- Never guess IDs, dates, wallet numbers, mobile numbers, transaction IDs, or program manager IDs.
- If required information is missing, ask the user for only the missing details.
- Keep follow-up questions short, clear, and business-friendly.
""".strip()