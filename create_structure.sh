#!/bin/bash

# Root folder
ROOT="wallet-agent"

# Create directories
mkdir -p $ROOT/app/api
mkdir -p $ROOT/app/core
mkdir -p $ROOT/app/memory
mkdir -p $ROOT/app/models
mkdir -p $ROOT/app/mcp
mkdir -p $ROOT/app/agents
mkdir -p $ROOT/app/services
mkdir -p $ROOT/app/schemas
mkdir -p $ROOT/configs
mkdir -p $ROOT/tests

# Create files

# app/api
touch $ROOT/app/api/routes_chat.py

# app/core
touch $ROOT/app/core/config.py
touch $ROOT/app/core/logging.py
touch $ROOT/app/core/exceptions.py

# app/memory
touch $ROOT/app/memory/state.py
touch $ROOT/app/memory/checkpointer.py
touch $ROOT/app/memory/summarizer.py

# app/models
touch $ROOT/app/models/llm_factory.py
touch $ROOT/app/models/provider_config.py

# app/mcp
touch $ROOT/app/mcp/client.py
touch $ROOT/app/mcp/tool_groups.py
touch $ROOT/app/mcp/tool_aliases.py
touch $ROOT/app/mcp/tool_filter.py

# app/agents
touch $ROOT/app/agents/prompts.py
touch $ROOT/app/agents/router.py
touch $ROOT/app/agents/agent_factory.py
touch $ROOT/app/agents/context_builder.py

# app/services
touch $ROOT/app/services/chat_service.py
touch $ROOT/app/services/state_service.py

# app/schemas
touch $ROOT/app/schemas/chat.py
touch $ROOT/app/schemas/state.py

# app root file
touch $ROOT/app/main.py

# configs
touch $ROOT/configs/model_config.yaml

# tests
touch $ROOT/tests/test_router.py
touch $ROOT/tests/test_tool_filter.py
touch $ROOT/tests/test_chat_api.py

# root files
touch $ROOT/.env
touch $ROOT/requirements.txt
touch $ROOT/README.md

echo "Folder structure created successfully!"