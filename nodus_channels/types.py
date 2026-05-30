"""Core channel data types: Peer, Attachment, Message, ChannelInfo."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Peer:
    """Identity of a person or entity within a specific channel.

    Attributes
    ----------
    id:           Platform-native peer ID (e.g. Slack user ID ``U0123``).
    channel_id:   The channel this peer belongs to (e.g. ``"slack"``).
    display_name: Human-readable name, if available.
    raw:          Platform-specific extra data (avatars, roles, etc.).
    """

    id: str
    channel_id: str
    display_name: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class Attachment:
    """A non-text file or media item attached to a message.

    Attributes
    ----------
    type:       Media category: ``"image"``, ``"video"``, ``"audio"``,
                ``"file"``, or ``"sticker"``.
    mime_type:  MIME type string (e.g. ``"image/png"``).
    url:        Download URL, if provided by the platform.
    content:    Raw bytes, if already fetched.
    filename:   Original filename.
    size_bytes: File size in bytes.
    """

    type: str
    mime_type: str | None = None
    url: str | None = None
    content: bytes | None = None
    filename: str | None = None
    size_bytes: int | None = None


@dataclass
class Message:
    """A normalized inbound message from any channel.

    Attributes
    ----------
    id:           Platform-native message ID.
    channel_id:   Which channel this message came from.
    sender:       The ``Peer`` who sent the message.
    content:      Normalized plain-text (or markdown) content.
    timestamp:    When the message was sent (timezone-aware).
    attachments:  Any attached files or media.
    reply_to_id:  ID of the message this is a reply to, if any.
    thread_id:    Thread or topic ID, if the channel supports threads.
    raw:          Platform-specific raw message payload.
    """

    id: str
    channel_id: str
    sender: Peer
    content: str
    timestamp: datetime
    attachments: list[Attachment] = field(default_factory=list)
    reply_to_id: str | None = None
    thread_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChannelInfo:
    """Static capabilities and limits for a channel.

    Attributes
    ----------
    id:                   Unique channel identifier (e.g. ``"slack"``, ``"discord"``).
    display_name:         Human-readable name.
    supports_threads:     Whether the channel supports threaded replies.
    supports_markdown:    Whether the channel renders markdown.
    max_message_length:   Character limit per message (default 4000).
    supports_attachments: Whether the channel accepts file uploads.
    """

    id: str
    display_name: str
    supports_threads: bool = False
    supports_markdown: bool = True
    max_message_length: int = 4000
    supports_attachments: bool = True
