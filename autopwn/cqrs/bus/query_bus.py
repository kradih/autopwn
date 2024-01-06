from typing import Type
from . import AbstractBus, AbstractHandler, AbstractMessage, BusResponse


class Query(AbstractMessage):
    """Abstract class for querys."""

    pass


class QueryHandler(AbstractHandler):
    """Abstract class for query handlers."""

    def __init__(self, message_type: Type[Query]) -> None:
        if not issubclass(message_type, Query):
            raise TypeError(
                "message_type must be a subclass of AbstractMessage"
            )
        super().__init__(message_type)


class QueryBus(AbstractBus):
    """Query bus implementation."""

    def register_query_handler(self, handler: QueryHandler) -> None:
        """Register a query handler."""
        if not isinstance(handler, QueryHandler):
            raise TypeError("handler must be an instance of QueryHandler")
        self._register(handler)

    def unregister_query_handler(self, message_type: Type[Query]) -> bool:
        """Unregister a query handler."""
        return self._unregister(message_type)

    async def query(self, query: Query) -> BusResponse:
        """Send a query."""
        return await self._send_message(query)
