import pytest

from pytest import fixture, raises
from unittest.mock import AsyncMock

from autopwn.cqrs.bus.event_bus import EventBus, EventHandler, Event


@fixture
def event_bus():
    return EventBus()


def test_register_none_event_handler_raises_exception(event_bus) -> None:
    with raises(TypeError):
        event_bus.register_event_handler(None)


@pytest.mark.asyncio
async def test_register_event_handler(event_bus) -> None:
    class TestEvent(Event):
        def __init__(self, test: str):
            self.test = test

    class TestEventHandler(EventHandler):
        async def handle(self, message: TestEvent) -> None:
            pass

    test_event_handler1 = TestEventHandler(TestEvent)
    event_bus.register_event_handler(test_event_handler1)

    response = await event_bus.register_event(TestEvent("test1"))
    assert response.success

    response = await event_bus.register_event(TestEvent("test2"))
    assert response.success

    response = await event_bus.register_event("")
    assert not response.success


@pytest.mark.asyncio
async def test_handle_called_to_all_registered_handlers(event_bus) -> None:
    class TestEvent(Event):
        def __init__(self, test: str):
            self.test = test

    class TestEventHandler1(EventHandler):
        async def handle(self, message: TestEvent) -> None:
            pass

    class TestEventHandler2(EventHandler):
        async def handle(self, message: TestEvent) -> None:
            pass

    test_event_handler1 = TestEventHandler1(TestEvent)
    test_event_handler1.handle = AsyncMock()

    test_event_handler2 = TestEventHandler2(TestEvent)
    test_event_handler2.handle = AsyncMock()

    event_bus.register_event_handler(test_event_handler1)
    event_bus.register_event_handler(test_event_handler2)

    await event_bus.register_event(TestEvent("test1"))
    test_event_handler1.handle.assert_called_once()
    test_event_handler2.handle.assert_called_once()
