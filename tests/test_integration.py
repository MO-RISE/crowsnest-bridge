import time
import threading
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest
from paho.mqtt import publish, subscribe


@contextmanager
def subscriber(*args, **kwargs):
    t = threading.Thread(target=subscribe.callback, args=args, kwargs=kwargs)
    t.setDaemon(True)
    t.start()
    time.sleep(0.1)
    yield


@pytest.mark.parametrize("first,second", [(1881, 1882), (1882, 1881)])
def test_simple_forwarding_with_forwarded_topic(compose, first, second):

    mock = MagicMock()

    with subscriber(mock, "/any/topic/#", hostname="localhost", port=first):
        publish.single("/any/topic/here", "payload", hostname="localhost", port=second)
        time.sleep(0.1)

    mock.assert_called_once()
    args, _ = mock.call_args
    _, _, message = args
    assert message.topic == "/any/topic/here"
    assert message.payload.decode() == "payload"


@pytest.mark.parametrize("first,second", [(1881, 1882), (1882, 1881)])
def test_simple_forwarding_with_not_forwarded_topic(compose, first, second):

    mock = MagicMock()

    with subscriber(mock, "/other/topic/#", hostname="localhost", port=first):
        publish.single(
            "/other/topic/here", "payload", hostname="localhost", port=second
        )
        time.sleep(0.1)

    mock.assert_not_called()
