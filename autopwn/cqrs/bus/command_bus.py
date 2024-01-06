from typing import Type
from . import AbstractBus, AbstractHandler, AbstractMessage, BusResponse


class Command(AbstractMessage):
    """Abstract class for commands."""

    pass


class CommandHandler(AbstractHandler):
    """Abstract class for command handlers."""

    def __init__(self, message_type: Type[Command]) -> None:
        if not issubclass(message_type, Command):
            raise TypeError(
                "message_type must be a subclass of AbstractMessage"
            )
        super().__init__(message_type)


class CommandBus(AbstractBus):
    """Command bus implementation."""

    def register_command_handler(self, handler: CommandHandler) -> None:
        """Register a command handler."""
        if not isinstance(handler, CommandHandler):
            raise TypeError("handler must be an instance of CommandHandler")
        self._register(handler)

    def unregister_command_handler(self, message_type: Type[Command]) -> bool:
        """Unregister a command handler."""
        return self._unregister(message_type)

    async def send_command(self, command: Command) -> BusResponse:
        """Send a command."""
        return await self._send_message(command)
