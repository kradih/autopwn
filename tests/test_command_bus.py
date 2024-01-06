import pytest

from pytest import fixture, raises
from autopwn.cqrs.bus.command_bus import CommandBus, CommandHandler, Command


@fixture
def command_bus():
    return CommandBus()


def test_register_none_command_handler_raises_exception(command_bus) -> None:
    with raises(TypeError):
        command_bus.register_command_handler(None)


@pytest.mark.asyncio
async def test_register_command_handler(command_bus) -> None:
    class TestCommand(Command):
        def __init__(self, test: str):
            self.test = test

    class TestCommandHandler(CommandHandler):
        async def handle(self, message: TestCommand) -> str:
            return message.test

    test_command_handler = TestCommandHandler(TestCommand)
    command_bus.register_command_handler(test_command_handler)
    assert (
        command_bus._AbstractBus__handlers[TestCommand] == test_command_handler
    )

    response = await command_bus.send_command(TestCommand("test1"))
    assert response.success
    assert response.message == "test1"

    response = await command_bus.send_command(TestCommand("test2"))
    assert response.success
    assert response.message == "test2"

    response = await command_bus.send_command("")
    assert not response.success
