import threading
from nodus_channels import ChannelInfo, ChannelRegistry


class _StubAdapter:
    def __init__(self, cid):
        self._id = cid
    @property
    def channel_id(self): return self._id
    @property
    def info(self): return ChannelInfo(id=self._id, display_name=self._id.title())
    async def connect(self): pass
    async def disconnect(self): pass
    async def send(self, content, peer_id, **_): return "msg-id"
    def subscribe(self): ...
    async def health_check(self): return True


def test_register_and_get():
    r = ChannelRegistry()
    a = _StubAdapter("slack")
    r.register(a)
    assert r.get("slack") is a


def test_get_unknown_returns_none():
    r = ChannelRegistry()
    assert r.get("discord") is None


def test_len():
    r = ChannelRegistry()
    assert len(r) == 0
    r.register(_StubAdapter("slack"))
    r.register(_StubAdapter("discord"))
    assert len(r) == 2


def test_contains():
    r = ChannelRegistry()
    r.register(_StubAdapter("slack"))
    assert "slack" in r
    assert "discord" not in r


def test_unregister():
    r = ChannelRegistry()
    r.register(_StubAdapter("slack"))
    assert r.unregister("slack") is True
    assert r.get("slack") is None
    assert r.unregister("slack") is False


def test_list_returns_all():
    r = ChannelRegistry()
    r.register(_StubAdapter("a"))
    r.register(_StubAdapter("b"))
    ids = {a.channel_id for a in r.list()}
    assert ids == {"a", "b"}


def test_register_overwrites():
    r = ChannelRegistry()
    a1 = _StubAdapter("slack")
    a2 = _StubAdapter("slack")
    r.register(a1)
    r.register(a2)
    assert r.get("slack") is a2
    assert len(r) == 1


def test_thread_safe():
    r = ChannelRegistry()
    errors = []
    def worker(n):
        try:
            for i in range(5):
                r.register(_StubAdapter(f"ch_{n}_{i}"))
        except Exception as e:
            errors.append(e)
    threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors
