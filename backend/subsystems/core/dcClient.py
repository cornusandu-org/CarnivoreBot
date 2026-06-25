import discord
from .logManager import getLogger
from .logErrors import LogErrors
from .assetManager import AssetManager
from typing import Callable, Coroutine, Literal

logger = getLogger("dcClient")

client: discord.Client = None

listeners = {
    'onMessage': []
}

async def startClient(cl: discord.Client, token: str):
    global client
    client = cl

    client.event(on_ready)
    client.event(on_message)
    
    with LogErrors('dcClient', True):
        logger.debug("Starting bot...")
        await client.start(token)

#@client.event
async def on_ready():
    logger.success(f"Started bot: {client.user.name} (#{client.user.id})")

async def on_message(message: discord.Message):
    #logger.debug(f'Recieved message: {message.content}')
    for listener in listeners['onMessage']:
        with LogErrors('dcClient:on_message'):
            await listener(message)

def registerCommand(cmd: str, handler: Callable[[discord.Message], Coroutine], includePrefix: bool = True):
    logger.debug(f"Registered command: '{cmd}'. Prefix: {'enabled' if includePrefix else 'disabled'}")

    async def wrapper(message: discord.Message):
        prefix = AssetManager.settings['Discord']['Command']['Prefix'] if includePrefix else ''
        
        if not message.content.startswith(prefix):
            return
        
        if not message.content.startswith(f"{prefix}{cmd}"):
            logger.warning(f"Ignoring command: '{message.content}'. Cause: No handler installed.")
            return

        await handler(message)
        
    listeners['onMessage'].append(wrapper)

def registerHandler(event: Literal['onMessage'], handler: Callable[[discord.Message], Coroutine]):
    listeners[event].append(handler)
