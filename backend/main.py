from subsystems.feat import pingPong
from subsystems.core.dcClient import startClient
from subsystems.core.assetManager import AssetManager
import discord

import asyncio

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Client(intents = intents)


    pingPong.InitialisePingPongCommand()

    await startClient(bot, AssetManager.settings['Discord']['App']['Auth']['AuthToken'])
    await asyncio.Event().wait()

asyncio.run(main())
