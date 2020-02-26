import asyncio
import aiohttp_cors
from aiohttp import web
from routes import setup_routes


def initApp():
    app = web.Application()
    setup_routes(app)

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

    return app

def main():
    import sys
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    print('输出为 utf-8')
    
    app = initApp()
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    main()