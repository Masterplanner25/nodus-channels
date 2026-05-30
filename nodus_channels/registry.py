"""ChannelRegistry — thread-safe registry of active channel adapters."""
from __future__ import annotations

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adapter import ChannelAdapter


class ChannelRegistry:
    """Thread-safe registry of ``ChannelAdapter`` instances.

    Usage::

        registry = ChannelRegistry()
        registry.register(my_slack_adapter)
        adapter = registry.get("slack")

        for adapter in registry.list():
            await adapter.connect()
    """

    def __init__(self) -> None:
        self._adapters: dict[str, "ChannelAdapter"] = {}
        self._lock = threading.Lock()

    def register(self, adapter: "ChannelAdapter") -> None:
        """Register *adapter*.  Overwrites any existing entry for the same channel_id."""
        with self._lock:
            self._adapters[adapter.channel_id] = adapter

    def get(self, channel_id: str) -> "ChannelAdapter | None":
        """Return the adapter for *channel_id*, or None if not registered."""
        with self._lock:
            return self._adapters.get(channel_id)

    def list(self) -> "list[ChannelAdapter]":
        """Return all registered adapters."""
        with self._lock:
            return list(self._adapters.values())

    def unregister(self, channel_id: str) -> bool:
        """Remove the adapter for *channel_id*. Returns True if it existed."""
        with self._lock:
            return self._adapters.pop(channel_id, None) is not None

    def __contains__(self, channel_id: str) -> bool:
        with self._lock:
            return channel_id in self._adapters

    def __len__(self) -> int:
        with self._lock:
            return len(self._adapters)
