from flask import Flask
from .logManager import getLogger

def getApp(name):
    app = Flask(f"CarnivoreBot:{name}")
    getLogger("flaskApp").debug(f"Created Flask app '{app.name}'")
    
    return app

def mkResponse(code: int, **values) -> dict[str, any]:
    return {
        "code": code,
        **values
    }

import flask.cli

flaskcliserverbannerlogger = getLogger("flaskBanner")
def custom_banner(debug: bool, app_import_path: str) -> None:
    flaskcliserverbannerlogger.debug(f"Flask '{app_import_path}' started. Debug = {'on' if debug else 'off'}")

flask.cli.show_server_banner = custom_banner
