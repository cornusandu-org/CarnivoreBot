from ..core import logManager
from ..core.suppressErrors import SuppressErrors
from ..core.logErrors import LogErrors
from ..core.assetManager import AssetManager
from ..core.flaskApp import getApp, mkResponse
from ..core.runtimeDataManager import readData, writeData, readSubsystem, writeSubsystem, popData
from ..core.featManager import start_feat

from flask import jsonify, request
from datetime import datetime, timedelta

class PingPongCommand:
    def __init__(self):
        self.app = getApp("PingPongCommand")

    async def init(self):
        self.app.add_url_rule('/api/userRatelimits/pingPong', view_func=self.handleRateLimit, methods=['GET', 'POST', 'REFRESH'])
        self.app.run(host='localhost', port = AssetManager.settings['Local']['Backend']['Port'], debug = False)

    async def handleRateLimit(self):
        now = datetime.now()
        
        match request.method:
            case 'GET':
                data = request.get_json()
                with SuppressErrors():
                    with LogErrors('pingPong:Get'):
                        userId = data.get('userId', None)
                        if isinstance(userId, str):
                            userId = int(userId)

                        ratelimit: datetime = await readData("feat:PingPong:ratelimit", userId) or datetime.fromisoformat('0001-01-01T01:01:01')

                        if (v := (ratelimit - now).total_seconds()) >= 0:
                            return jsonify(mkResponse(0, timeLeft = v, rateLimit = ratelimit))
                        else:
                            return jsonify(mkResponse(0, timeLeft = 0, rateLimit = now))
                    
            case 'POST':
                data = request.get_json()
                with SuppressErrors(), LogErrors('pingPong:Post'):
                    userId = data.get('userId', None)
                    if isinstance(userId, str):
                        userId = int(userId)
                    
                    await writeData("feat:PingPong:ratelimit", userId, now + timedelta(seconds = 3))

                    return jsonify(mkResponse(0))
                
            case 'REFRESH':
                ratelimits = await readSubsystem("feat:PingPong:ratelimit")
                for (userId, ratelimit) in ratelimits.items():
                    if (now >= ratelimit):
                        await popData("feat:PingPong:ratelimit", userId)

                return jsonify(mkResponse(0))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
