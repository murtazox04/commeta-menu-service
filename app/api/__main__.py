import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import load_config
from app.api import controllers, dependencies
from app.infrastructure.database.factory import create_pool, make_connection_string


def main() -> FastAPI:
    settings = load_config()
    app = FastAPI(
        version="1.0.0"
    )
    pool = create_pool(url=make_connection_string(settings=settings))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    dependencies.setup(app, pool, settings)
    controllers.setup(app)
    return app


app = main()

if __name__ == '__main__':
    uvicorn.run(
        "app.api.__main__:app",
        host="0.0.0.0",  # or your desired host
        port=8001,  # or your desired port
        # reload=True  # if you want to enable automatic reload
    )
