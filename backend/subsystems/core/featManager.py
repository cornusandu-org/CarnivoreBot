import threading
from .dependencies import sys
from . import logManager
import asyncio

logger = logManager.getLogger("featManager")

def start_feat(name: str, target, args, kwargs, daemon: bool = True) -> threading.Thread:
    if sys._is_gil_enabled():
        logger.warning("GIL is enabled.")

    def wrapper():
        l = logManager.getLogger("featManagerWrapper")
        l.info("Initialising")
        feat = target()
        asyncio.run(feat.init())
        l.success("Initialised")

    newThread = threading.Thread(target = wrapper, name = name, args = args, kwargs = kwargs, daemon = daemon)

    return newThread
