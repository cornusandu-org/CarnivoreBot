from discord import Message
from abc import ABC, abstractmethod

class CommandABC:
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def init(self):
        ...

    @abstractmethod
    async def onRunCommand(self, message: Message) -> None:
        ...
