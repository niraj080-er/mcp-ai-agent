from __future__ import annotations

from app.agents.prompts import SYSTEM_PROMPT
from app.memory.checkpointer import get_checkpointer

try:
    from langchain.agents import create_agent as _create_agent
    AGENT_API = "langchain_create_agent"
except ImportError:
    from langgraph.prebuilt import create_react_agent as _create_agent
    AGENT_API = "langgraph_create_react_agent"


def build_agent(llm, tools, extra_context: str):
    checkpointer = get_checkpointer()
    prompt = f"{SYSTEM_PROMPT}\n\n{extra_context}"

    if AGENT_API == "langchain_create_agent":
        return _create_agent(
            model=llm,
            tools=tools,
            system_prompt=prompt,
            checkpointer=checkpointer,
        )

    return _create_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        checkpointer=checkpointer,
    )