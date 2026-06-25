from .dependencies import *
from . import logManager

logger = logManager.getLogger("assetManager")

@lambda _: _()
class AssetManager:
    def __init__(self):
        logger.info('Initialising...')
        self.rootPath = pathlib.Path(__file__).parent.parent.parent.parent
        logger.success('Initialised')

    @cached_property
    def backendPath(self):
        logger.debug('Dereferencing backendPath')
        return self.rootPath / "backend"
    
    @cached_property
    def corePath(self):
        logger.debug('Dereferencing corePath')
        return self.backendPath / "core"
    
    @cached_property
    def settings(self):
        logger.debug('Dereferencing settings')
        try:
            with open(self.rootPath / "config.toml", 'rb') as f:
                return toml.load(f)
        except Exception as e:
            logger.critical('Failed to load settings.')
            logger.critical(e, exc_info=True, stack_info=True, stacklevel=3)
