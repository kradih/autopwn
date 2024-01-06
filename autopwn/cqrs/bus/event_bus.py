from typing import Dict, List, Type
from . import AbstractHandler, AbstractMessage, BusResponse


class Event(AbstractMessage):
    """Abstract class for events."""

    pass


class EventHandler(AbstractHandler):
    """Abstract class for event handlers."""

    def __init__(self, message_type: Type[Event]) -> None:
        if not issubclass(message_type, Event):
            raise TypeError(
                "message_type must be a subclass of AbstractMessage"
            )
        super().__init__(message_type)


class EventBus:
    """Event bus implementation."""

    def __init__(self) -> None:
        self.handlers: Dict[Type[Event], List[EventHandler]] = {}

    def register_event_handler(self, handler: EventHandler) -> None:
        """Register a event handler."""
        if not isinstance(handler, EventHandler):
            raise TypeError("handler must be an instance of EventHandler")
        if handler.message_type not in self.handlers:
            self.handlers[handler.message_type] = []
        self.handlers[handler.message_type].append(handler)

    def unregister_event_handler(self, handler: EventHandler) -> bool:
        """Unregister a event handler."""
        if handler.message_type in self.handlers:
            self.handlers[handler.message_type].remove(handler)
            return True
        return False

    async def register_event(self, event: Event) -> BusResponse:
        """Send a event."""
        if type(event) in self.handlers:
            for handler in self.handlers[type(event)]:
                await handler.handle(event)
            return BusResponse.ok(None)
        return BusResponse.fail(None)
