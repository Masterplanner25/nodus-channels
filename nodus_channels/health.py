"""Channel health monitoring — track connection status per channel."""
from __future__ import annotations

import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


class ChannelHealth:
    """Channel health status constants."""

    CONNECTED    = "connected"
    DEGRADED     = "degraded"      # recent failures, still operating
    DISCONNECTED = "disconnected"


@dataclass
class HealthSnapshot:
    """Snapshot of a channel's health at a point in time.

    Attributes
    ----------
    channel_id:    Which channel this is for.
    status:        One of the ``ChannelHealth`` constants.
    last_success:  UTC timestamp of the last successful operation.
    failure_count: Total consecutive failures since last success.
    last_error:    Most recent error message, if any.
    """

    channel_id: str
    status: str
    last_success: Optional[datetime]
    failure_count: int
    last_error: Optional[str]

    @property
    def is_healthy(self) -> bool:
        return self.status == ChannelHealth.CONNECTED


class HealthMonitor:
    """Track per-channel health state.

    Usage::

        monitor = HealthMonitor()
        monitor.record_success("slack")
        monitor.record_failure("discord", "connection refused")
        snap = monitor.snapshot("slack")   # status="connected"
    """

    _DEGRADED_THRESHOLD = 3   # failures before DEGRADED
    _DEAD_THRESHOLD = 10      # failures before DISCONNECTED

    def __init__(self) -> None:
        self._state: dict[str, dict] = {}
        self._lock = threading.Lock()

    def record_success(self, channel_id: str) -> None:
        """Record a successful operation for *channel_id*."""
        with self._lock:
            self._state[channel_id] = {
                "status": ChannelHealth.CONNECTED,
                "last_success": datetime.now(timezone.utc),
                "failure_count": 0,
                "last_error": None,
            }

    def record_failure(self, channel_id: str, error: str) -> None:
        """Record a failed operation for *channel_id*."""
        with self._lock:
            prev = self._state.get(channel_id, {})
            count = prev.get("failure_count", 0) + 1
            if count >= self._DEAD_THRESHOLD:
                status = ChannelHealth.DISCONNECTED
            elif count >= self._DEGRADED_THRESHOLD:
                status = ChannelHealth.DEGRADED
            else:
                status = prev.get("status", ChannelHealth.DEGRADED)
            self._state[channel_id] = {
                "status": status,
                "last_success": prev.get("last_success"),
                "failure_count": count,
                "last_error": error,
            }

    def snapshot(self, channel_id: str) -> HealthSnapshot:
        """Return the current health snapshot for *channel_id*.

        Returns a ``DISCONNECTED`` snapshot with zero history if the channel
        has never been registered.
        """
        with self._lock:
            state = self._state.get(channel_id, {})
        return HealthSnapshot(
            channel_id=channel_id,
            status=state.get("status", ChannelHealth.DISCONNECTED),
            last_success=state.get("last_success"),
            failure_count=state.get("failure_count", 0),
            last_error=state.get("last_error"),
        )

    def all_snapshots(self) -> list[HealthSnapshot]:
        """Return health snapshots for all tracked channels."""
        with self._lock:
            channel_ids = list(self._state.keys())
        return [self.snapshot(cid) for cid in channel_ids]

    def is_healthy(self, channel_id: str) -> bool:
        """Return True if the channel's last recorded status is CONNECTED."""
        return self.snapshot(channel_id).status == ChannelHealth.CONNECTED
