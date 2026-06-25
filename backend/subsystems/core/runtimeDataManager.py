from threading import RLock
from .suppressErrors import SuppressErrors
from .logErrors import LogErrors

import copy

data: dict[str, dict[any, any]] = {}
data_lock = RLock()

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
