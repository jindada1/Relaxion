import asyncio
import aiohttp_cors
from aiohttp import web
from routes import setup_routes
from settings import load_configuration

def set_cors(app):
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
            )
    })
    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

def main():
    # load configurations
    config = load_configuration('./config.yml')
    # create web instance
    app = web.Application()
    # setup routes
    setup_routes(app, config)
    # config CORS
    set_cors(app)

    web.run_app(app, host=config['host'], port=config['port'])

if __name__ == '__main__':
    main()