"""ChannelAdapter — structural protocol for all channel implementations."""
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]

if TYPE_CHECKING:
    from .types import Attachment, ChannelInfo, Message


@runtime_checkable
class ChannelAdapter(Protocol):
    """Structural protocol that all concrete channel adapters must satisfy.

    Concrete adapters (Slack, Discord, Telegram, etc.) are separate packages
    that implement this protocol.  Register them with ``ChannelRegistry``.

    Usage::

        class SlackAdapter:
            @property
            def channel_id(self) -> str: return "slack"
            # ... implement all methods ...

        registry = ChannelRegistry()
        registry.register(SlackAdapter(...))
    """

    @property
    def channel_id(self) -> str:
        """Unique identifier for this channel (e.g. ``"slack"``, ``"discord"``)."""
        ...

    @property
    def info(self) -> "ChannelInfo":
        """Static capabilities and limits for this channel."""
        ...

    async def connect(self) -> None:
        """Open the connection to the platform."""
        ...

    async def disconnect(self) -> None:
        """Close the connection gracefully."""
        ...

    async def send(
        self,
        content: str,
        peer_id: str,
        *,
        thread_id: str | None = None,
        reply_to_id: str | None = None,
        attachments: "list[Attachment] | None" = None,
    ) -> str:
        """Send a message to *peer_id*.

        Args:
            content:      Text (or markdown) to send.
            peer_id:      Platform-native recipient ID.
            thread_id:    Optional thread/topic to post in.
            reply_to_id:  Optional message to quote/reply to.
            attachments:  Optional list of attachments.

        Returns:
            Platform-native message ID of the sent message.
        """
        ...

    def subscribe(self) -> "AsyncIterator[Message]":
        """Yield inbound ``Message`` objects as they arrive."""
        ...

    async def health_check(self) -> bool:
        """Return True if the channel is reachable and functional."""
        ...
