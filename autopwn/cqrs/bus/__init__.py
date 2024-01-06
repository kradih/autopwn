from abc import ABC, abstractmethod
from typing import Dict, Type


class AbstractMessage(ABC):
    """Abstract class for messages."""

    pass


class BusResponse:
    """Class for handler responses."""

    def __init__(self, success: bool, message: any) -> None:
        self.success = success
        self.message = message

    @staticmethod
    def ok(message: any) -> "BusResponse":
        """Return a successful response."""
        return BusResponse(True, message)

    @staticmethod
    def fail(message: any) -> "BusResponse":
        """Return a failed response."""
        return BusResponse(False, message)


class AbstractHandler(ABC):
    """Abstract class for handlers."""

    def __init__(self, message_type: Type[AbstractMessage]) -> None:
        if not issubclass(message_type, AbstractMessage):
            raise TypeError(
                "message_type must be a subclass of AbstractMessage"
            )
        self.message_type = message_type

    @property
    def message_type(self) -> Type[AbstractMessage]:
        return self.__message_type

    @message_type.setter
    def message_type(self, message_type: Type[AbstractMessage]):
        self.__message_type = message_type

    @abstractmethod
    async def handle(self, message) -> any:
        """Handle a message."""
        pass


class AbstractBus(ABC):
    """Abstract class for buses."""

    def __init__(self) -> None:
        super().__init__()
        self.__handlers: Dict[Type[AbstractMessage], AbstractHandler] = {}

    def _register(self, handler: AbstractHandler) -> None:
        """Register a handler for a message type."""
        if not isinstance(handler, AbstractHandler):
            raise TypeError("handler must be an instance of AbstractHandler")
        self.__handlers[handler.message_type] = handler

    def _unregister(self, message_type: Type[AbstractMessage]) -> bool:
        """Unregister a handler for a message type."""
        if message_type in self.__handlers:
            del self.__handlers[message_type]
            return True
        return False

    async def _send_message(self, message: AbstractMessage) -> BusResponse:
        """Send a message to the appropriate handler."""
        if type(message) in self.__handlers:
            return BusResponse.ok(
                await self.__handlers[type(message)].handle(message)
            )
        return BusResponse.fail("Not found")
