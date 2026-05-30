"""nodus-channels — multi-channel messaging protocol and core types.

Defines the standard vocabulary for multi-channel AI systems: normalized
message types, a channel adapter protocol, a thread-safe registry, and
per-channel health monitoring.

Concrete channel adapters (Slack, Discord, Telegram, etc.) are separate
packages that implement the ``ChannelAdapter`` protocol.

Types:
    Peer          — messaging identity within a channel
    Attachment    — file/media attached to a message
    Message       — normalized inbound message from any channel
    ChannelInfo   — static capabilities and limits for a channel

Adapter protocol:
    ChannelAdapter  — protocol all concrete adapters must satisfy

Registry:
    ChannelRegistry  — thread-safe adapter registry

Health:
    ChannelHealth    — status constants (CONNECTED | DEGRADED | DISCONNECTED)
    HealthSnapshot   — point-in-time health for one channel
    HealthMonitor    — record success/failure and query status
"""
from .adapter import ChannelAdapter
from .health import ChannelHealth, HealthMonitor, HealthSnapshot
from .registry import ChannelRegistry
from .types import Attachment, ChannelInfo, Message, Peer

__all__ = [
    # Types
    "Peer",
    "Attachment",
    "Message",
    "ChannelInfo",
    # Protocol
    "ChannelAdapter",
    # Registry
    "ChannelRegistry",
    # Health
    "ChannelHealth",
    "HealthSnapshot",
    "HealthMonitor",
]
