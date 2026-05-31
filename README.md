# nodus-channels

**Multi-channel messaging protocol and core types for Nodus AI systems.**

Defines the standard vocabulary for multi-channel AI assistants: normalized
message types, a channel adapter protocol, a thread-safe registry, and
per-channel health monitoring. Concrete adapters (Slack, Discord, Telegram,
webhook, etc.) are separate packages that implement the `ChannelAdapter`
protocol.

No required external dependencies — pure stdlib.

> **Status:** v0.1.0 — prepared, not yet published.

---

## Install

```bash
pip install nodus-channels
```

---

## What it provides

| Component | Purpose |
|---|---|
| `Message` / `Peer` / `Attachment` / `ChannelInfo` | Normalized inbound message types |
| `ChannelAdapter` | Protocol all concrete adapters must satisfy |
| `ChannelRegistry` | Thread-safe adapter registry |
| `HealthMonitor` / `HealthSnapshot` / `ChannelHealth` | Per-channel health tracking |

---

## Core types

```python
from nodus_channels import Message, Peer, Attachment, ChannelInfo

peer = Peer(id="U123", display_name="Alice", channel_id="slack")

msg = Message(
    id="msg-001",
    channel_id="slack",
    peer=peer,
    text="Hello, agent!",
    attachments=[Attachment(url="https://...", media_type="image/png")],
)

info = ChannelInfo(
    id="slack",
    display_name="Slack",
    max_message_length=4000,
    supports_threads=True,
    supports_attachments=True,
)
```

---

## ChannelAdapter protocol

Concrete adapters implement this protocol:

```python
from nodus_channels import ChannelAdapter, ChannelInfo, Message
from typing import AsyncIterator

class SlackAdapter:
    @property
    def channel_id(self) -> str: return "slack"

    @property
    def info(self) -> ChannelInfo:
        return ChannelInfo(id="slack", display_name="Slack")

    async def send(self, content: str, peer_id: str, **kwargs) -> str:
        # returns message ID
        ...

    def subscribe(self) -> AsyncIterator[Message]:
        # yields inbound messages
        ...

assert isinstance(SlackAdapter(), ChannelAdapter)  # runtime_checkable
```

`ChannelAdapter` is a `@runtime_checkable` Protocol — `isinstance` checks work
without inheritance.

---

## ChannelRegistry

```python
from nodus_channels import ChannelRegistry

registry = ChannelRegistry()
registry.register(slack_adapter)
registry.register(discord_adapter)

adapter = registry.get("slack")          # ChannelAdapter | None
all_adapters = registry.list_all()       # list[ChannelAdapter]
registry.unregister("slack")
len(registry)
```

Thread-safe — safe to register/unregister from multiple threads.

---

## HealthMonitor

```python
from nodus_channels import HealthMonitor, ChannelHealth

monitor = HealthMonitor()
monitor.record_success("slack")
monitor.record_failure("discord", reason="connection refused")

snap = monitor.snapshot("slack")
# snap.status     → ChannelHealth.CONNECTED
# snap.failure_count → 0
# snap.last_error    → None

snap2 = monitor.snapshot("discord")
# snap2.status → ChannelHealth.DEGRADED or DISCONNECTED
```

Health status transitions:
- `CONNECTED` — no recent failures
- `DEGRADED` — some failures, but also recent successes
- `DISCONNECTED` — only failures, no recent success

---

## Design

- **No required dependencies.** Pure stdlib (`threading`, `dataclasses`,
  `datetime`, `typing`).
- **Protocol-based.** `ChannelAdapter` is `@runtime_checkable` — adapters
  satisfy it by structure, not inheritance.
- **Thread-safe.** `ChannelRegistry` uses `threading.Lock`.

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

---

## License

MIT — see [LICENSE](LICENSE).
