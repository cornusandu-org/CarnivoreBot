import subsystems.core.assetManager as assetManager
import subsystems.core.featManager as featManager
import subsystems.core.logErrors as logErrors
import subsystems.core.suppressErrors as suppressErrors

async def main():
    a = assetManager.AssetManager()
    
    with logErrors.LogErrors('mainInitFeat', True):
        featManager.start_feat(None)

    a.settings

import asyncio
asyncio.run(main())
