from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api import api_router
from src.config import app_configs, settings
from src.db.session import sessionmanager


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    logger.debug("Starting the app...")
    yield
    # Shutdown
    logger.debug("Stopping the app...")
    if sessionmanager.engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


app.include_router(api_router, prefix="/api")


@app.exception_handler(Exception)
async def generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": [
                {"msg": "Something went wrong", "loc": ["Unknown"], "type": "Unknown"}
            ]
        },
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.debug(f"Validation Error: {exc!s}")
    return JSONResponse(
        content=jsonable_encoder({"detail": exc.errors()}),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
