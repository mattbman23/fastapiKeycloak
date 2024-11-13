from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils import auth
from routers import minio, todo
from utils.logger import logger
from utils.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await init_db()
    yield
    logger.info("Closing application")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/health")
def get_public():
    return {"health": "healthy"}


# only authenticated users can access the route, need to pass valid jwt to header
app.include_router(minio.router, dependencies=[Depends(auth.valid_access_token)])
app.include_router(todo.router, dependencies=[Depends(auth.valid_access_token)])


# only users with admin role can access
@app.get("/admin", dependencies=[Depends(auth.has_role("admin"))])
def get_private():
    return {"message": "Admin only"}


# only users with standard role can access
@app.get("/standard", dependencies=[Depends(auth.has_role("standard"))])
def get_private():
    return {"message": "Standard only"}
