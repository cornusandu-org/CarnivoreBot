import threading
from .dependencies import sys
from . import logManager
import asyncio
from threading import RLock

logger = logManager.getLogger("featManager")

features = []
features_lock = RLock()

def start_feat(name: str, target, daemon: bool = True) -> threading.Thread:
    if sys._is_gil_enabled():
        logger.warning("The GIL is enabled. This may result in lower multithreaded performance.")

    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        l = logManager.getLogger("featManagerWrapper")
        l.info("Initialising")
        feat = target()

        loop.create_task(feat.init())

        with features_lock:
            features.append(feat)

        l.success("Initialised")

        try:
            loop.run_forever()
        except BaseException as e:
            logger.error(e)
            if loop.is_running():
                loop.stop()
        finally:
            loop.close()

    newThread = threading.Thread(target = wrapper, name = name, daemon = daemon)
    newThread.start()

    return newThread
