# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.0] — 2026-05-30

Initial release — prepared, not yet published.

### Added

- **`Peer`** — messaging identity within a channel. Fields: `id`,
  `display_name`, `channel_id`, optional `metadata`.

- **`Attachment`** — file or media attached to a message. Fields: `url`,
  `media_type`, optional `filename`, `size_bytes`.

- **`Message`** — normalized inbound message from any channel. Fields: `id`,
  `channel_id`, `peer`, `text`, `attachments`, `thread_id`, `reply_to_id`,
  `received_at`, `metadata`.

- **`ChannelInfo`** — static capabilities and limits for a channel. Fields:
  `id`, `display_name`, `max_message_length`, `supports_threads`,
  `supports_attachments`, `supports_reactions`.

- **`ChannelAdapter`** — `@runtime_checkable` Protocol. Required properties:
  `channel_id` (str) and `info` (ChannelInfo). Required methods: `send()`,
  `subscribe()`. Optional: `connect()`, `disconnect()`, `health_check()`.

- **`ChannelRegistry`** — thread-safe adapter registry. `register`,
  `unregister`, `get`, `list_all`, `len`.

- **`ChannelHealth`** — status constants: `CONNECTED`, `DEGRADED`,
  `DISCONNECTED`.

- **`HealthSnapshot`** — point-in-time health for one channel. Fields:
  `channel_id`, `status`, `failure_count`, `success_count`, `last_error`,
  `last_success_at`, `last_failure_at`.

- **`HealthMonitor`** — records success/failure events and derives health
  status. `record_success(channel_id)`, `record_failure(channel_id, reason)`,
  `snapshot(channel_id)`.

- **24 tests** across three test files (health, registry, types).

- **No required dependencies** — pure stdlib.

[0.1.0]: https://github.com/Masterplanner25/nodus-channels/releases/tag/v0.1.0
