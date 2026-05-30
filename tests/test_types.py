from datetime import datetime, timezone
from nodus_channels import Attachment, ChannelInfo, Message, Peer


def test_peer_creation():
    p = Peer(id="U123", channel_id="slack", display_name="Alice")
    assert p.id == "U123"
    assert p.channel_id == "slack"
    assert p.display_name == "Alice"
    assert p.raw == {}


def test_peer_raw_default_empty():
    p = Peer(id="x", channel_id="discord")
    assert p.raw == {}


def test_attachment_defaults():
    a = Attachment(type="image")
    assert a.mime_type is None
    assert a.url is None
    assert a.content is None


def test_message_creation():
    peer = Peer(id="U1", channel_id="slack")
    ts = datetime.now(timezone.utc)
    msg = Message(id="m1", channel_id="slack", sender=peer, content="hello", timestamp=ts)
    assert msg.id == "m1"
    assert msg.content == "hello"
    assert msg.attachments == []
    assert msg.reply_to_id is None
    assert msg.thread_id is None


def test_message_with_attachments():
    peer = Peer(id="U1", channel_id="slack")
    ts = datetime.now(timezone.utc)
    att = Attachment(type="image", mime_type="image/png")
    msg = Message(id="m2", channel_id="slack", sender=peer, content="pic", timestamp=ts, attachments=[att])
    assert len(msg.attachments) == 1
    assert msg.attachments[0].mime_type == "image/png"


def test_channel_info_defaults():
    info = ChannelInfo(id="slack", display_name="Slack")
    assert info.supports_threads is False
    assert info.supports_markdown is True
    assert info.max_message_length == 4000
    assert info.supports_attachments is True
