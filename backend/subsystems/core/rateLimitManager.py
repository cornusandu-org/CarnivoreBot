from .logManager import getLogger
from . import runtimeDataManager as RDM
from datetime import datetime, timedelta
from .dependencies import Any
from .logErrors import LogErrors
from .suppressErrors import SuppressErrors

async def addRateLimit(target: str | int | Any, command: str, time: timedelta) -> None:
    with SuppressErrors(), LogErrors():
        await RDM.writeData(f"rateLimitManager:{command}", target, datetime.now() + time)

async def getRateLimit(target: str | int | Any, command: str) -> timedelta:
    with SuppressErrors(), LogErrors():
        targetTime = await RDM.readData(f"rateLimitManager:{command}", target)

        if datetime.now() >= targetTime:
            return timedelta()

        timeLeft = targetTime - datetime.now() if targetTime > datetime.now() else 0

        return timeLeft
    
    return timedelta()

async def refreshRateLimits(command: str) -> bool:
    try:
        with LogErrors():
            ratelimits = await RDM.readSubsystem(f"rateLimitManager:{command}")
            for (identifier, targetTime) in ratelimits.items():
                if datetime.now() >= targetTime:
                    await RDM.popData(f"rateLimitManager:{command}", identifier)
            
            return True
        
    except Exception as e:
        return False
