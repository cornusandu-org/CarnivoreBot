from threading import RLock, Thread
import threading
from .suppressErrors import SuppressErrors
from .logErrors import LogErrors
from .logManager import getLogger
from time import sleep
import sys

import copy

data: dict[str, dict[any, any]] = {}
subsystem_size_limits: dict[str, int] = {}
data_lock = RLock()

def deepSize(value: dict | list, seen: set[int] | None = None) -> int:
    if seen is None:
        seen = set()

    if isinstance(value, list):
        return sum(map(lambda x: deepSize(x), value)) + sys.getsizeof(value)
    elif isinstance(value, dict):
        size = sys.getsizeof(value)

        for key in value.keys():
            size += sys.getsizeof(key)

        for value in value.values():
            size += deepSize(value, seen)

        return size
    elif isinstance(value, tuple):
        return sum(map(lambda x: deepSize(x), value)) + sys.getsizeof(value)
    elif isinstance(value, set):
        return sum(map(lambda x: deepSize(x), value)) + sys.getsizeof(value)
    else:
        return sys.getsizeof(value)

async def readData(subsystem: str, key: any) -> any:
    with data_lock:
        value = data.get(subsystem, {}).get(key)

    return value

async def readSubsystem(subsystem: str) -> dict[any, any] | None:
    with data_lock:
        value = data.get(subsystem)

    return copy.deepcopy(value)

async def writeSubsystem(subsystem: str, value: dict[any, any]) -> None:
    with data_lock:
        data[subsystem] = value

async def writeData(subsystem: str, key: any, value: any) -> None:
    with data_lock:
        if (data.get(subsystem, None) is None):
            data[subsystem] = {}
        data[subsystem][key] = value

async def popData(subsystem: str, key: any) -> None:
    with data_lock:
        if (v := data.get(subsystem)) is not None:
            with SuppressErrors(), LogErrors():
                v.pop(key)

def newThread():
    logger = getLogger("runtimeDataManager")
    while True:
        sleep(5)
        for (name, subsystem) in data.items():
            if deepSize(subsystem) >= subsystem_size_limits.get(name, 512) * 15:
                logger.critical(f"Size of runtime data subsystem {name} exceeds the limit of {subsystem_size_limits.get(name, 512)}B by 15x (or more), currently occupying {deepSize(subsystem)}B")
            elif deepSize(subsystem) >= subsystem_size_limits.get(name, 512):
                logger.warning(f"Size of runtime data subsystem {name} exceeds the limit of {subsystem_size_limits.get(name, 512)}B, currently occupying {deepSize(subsystem)}B")

if threading.current_thread() is threading.main_thread():
    Thread(target=newThread, name="runtimeDataManagerThread", daemon=True).start()
