class WalletAgentError(Exception):
    """Base exception for wallet-agent."""


class ConfigurationError(WalletAgentError):
    """Raised when configuration is invalid or missing."""


class DomainRoutingError(WalletAgentError):
    """Raised when routing fails."""


class MCPClientError(WalletAgentError):
    """Raised when MCP client/tool loading fails."""


class StateUpdateError(WalletAgentError):
    """Raised when state extraction/update fails."""