from ..core import logManager
from ..core.suppressErrors import SuppressErrors
from ..core.logErrors import LogErrors
from ..core.assetManager import AssetManager
from ..core import rateLimitManager
from ..core.featManager import start_feat
from ..core import dcClient

from datetime import datetime, timedelta

from discord import Message

class PingPongCommand:
    def __init__(self):
        dcClient.registerCommand("ping", self.onRunCommand)

    async def init(self):
        pass

    async def onRunCommand(self, message: Message) -> None:
        userId = message.author.id

        if (ratelimit := await rateLimitManager.getRateLimit(userId, "ping")) >= 0:
            await message.reply(f"You are being rate limited. Please wait {ratelimit.seconds} seconds before trying again.")

        await message.reply("Pong!")

        await rateLimitManager.addRateLimit(userId, "ping", timedelta(seconds=2))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
