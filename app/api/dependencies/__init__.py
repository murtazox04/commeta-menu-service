from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.config import Settings, load_config
from app.api.dependencies.settings import get_settings
from app.api.dependencies.database import DbProvider, dao_provider


def setup(
        app: FastAPI,
        pool: sessionmaker,
        settings: Settings,
):
    db_provider = DbProvider(pool=pool)
    app.dependency_overrides[dao_provider] = db_provider.dao
    app.dependency_overrides[get_settings] = load_config
