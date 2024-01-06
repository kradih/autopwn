import pytest

from pytest import fixture, raises
from autopwn.cqrs.bus.query_bus import QueryBus, QueryHandler, Query


@fixture
def query_bus():
    return QueryBus()


def test_register_none_query_handler_raises_exception(query_bus) -> None:
    with raises(TypeError):
        query_bus.register_query_handler(None)


@pytest.mark.asyncio
async def test_register_query_handler(query_bus) -> None:
    class TestQuery(Query):
        def __init__(self, test: str):
            self.test = test

    class TestQueryHandler(QueryHandler):
        async def handle(self, message: TestQuery) -> str:
            return message.test

    test_query_handler = TestQueryHandler(TestQuery)
    query_bus.register_query_handler(test_query_handler)
    assert query_bus._AbstractBus__handlers[TestQuery] == test_query_handler

    response = await query_bus.query(TestQuery("test1"))
    assert response.success
    assert response.message == "test1"

    response = await query_bus.query(TestQuery("test2"))
    assert response.success
    assert response.message == "test2"

    response = await query_bus.query("")
    assert not response.success
