from subsystems.feat import pingPong

import asyncio

async def main():
    pingPong.InitialisePingPongCommand()

    await asyncio.Event().wait()

asyncio.run(main())
