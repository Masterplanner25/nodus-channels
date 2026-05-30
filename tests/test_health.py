from nodus_channels import ChannelHealth, HealthMonitor


def test_unknown_channel_is_disconnected():
    m = HealthMonitor()
    snap = m.snapshot("slack")
    assert snap.status == ChannelHealth.DISCONNECTED
    assert snap.failure_count == 0
    assert snap.last_success is None


def test_record_success_makes_connected():
    m = HealthMonitor()
    m.record_success("slack")
    snap = m.snapshot("slack")
    assert snap.status == ChannelHealth.CONNECTED
    assert snap.failure_count == 0
    assert snap.last_success is not None


def test_record_failure_increments_count():
    m = HealthMonitor()
    m.record_success("slack")
    m.record_failure("slack", "timeout")
    snap = m.snapshot("slack")
    assert snap.failure_count == 1
    assert snap.last_error == "timeout"


def test_degraded_at_threshold():
    m = HealthMonitor()
    m.record_success("slack")
    for _ in range(3):
        m.record_failure("slack", "err")
    assert m.snapshot("slack").status == ChannelHealth.DEGRADED


def test_disconnected_at_high_threshold():
    m = HealthMonitor()
    m.record_success("slack")
    for _ in range(10):
        m.record_failure("slack", "err")
    assert m.snapshot("slack").status == ChannelHealth.DISCONNECTED


def test_is_healthy_true_after_success():
    m = HealthMonitor()
    m.record_success("slack")
    assert m.is_healthy("slack") is True


def test_is_healthy_false_after_failures():
    m = HealthMonitor()
    for _ in range(5):
        m.record_failure("slack", "err")
    assert m.is_healthy("slack") is False


def test_recovery_after_success():
    m = HealthMonitor()
    for _ in range(10):
        m.record_failure("slack", "err")
    assert m.snapshot("slack").status == ChannelHealth.DISCONNECTED
    m.record_success("slack")
    assert m.snapshot("slack").status == ChannelHealth.CONNECTED
    assert m.snapshot("slack").failure_count == 0


def test_all_snapshots():
    m = HealthMonitor()
    m.record_success("slack")
    m.record_failure("discord", "err")
    snaps = m.all_snapshots()
    ids = {s.channel_id for s in snaps}
    assert "slack" in ids
    assert "discord" in ids


def test_health_snapshot_is_healthy_property():
    m = HealthMonitor()
    m.record_success("ch")
    assert m.snapshot("ch").is_healthy is True
    m.record_failure("ch", "down")
    m.record_failure("ch", "down")
    m.record_failure("ch", "down")
    assert m.snapshot("ch").is_healthy is False
