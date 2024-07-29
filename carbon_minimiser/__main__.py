from carbon_minimiser.minimiser_api.app import create_app
import carbon_minimiser.config as CONFIG
from sanic import Sanic
from sanic.worker.loader import AppLoader
from functools import partial


def main(port):
    loader = AppLoader(factory=partial(create_app))
    app = loader.load()
    app.prepare(port=port)
    Sanic.serve(primary=app, app_loader=loader)
    
port = CONFIG.port

main(port)
