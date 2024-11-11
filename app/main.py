from fastapi import FastAPI, Depends
from utils import auth
from routers import minio

app = FastAPI()


@app.get("/health")
def get_public():
    return {"health": "healthy"}


# only authenticated users can access the route, need to pass valid jwt to header
app.include_router(minio.router, dependencies=[Depends(auth.valid_access_token)])


# only users with admin role can access
@app.get("/admin", dependencies=[Depends(auth.has_role("admin"))])
def get_private():
    return {"message": "Admin only"}


# only users with standard role can access
@app.get("/standard", dependencies=[Depends(auth.has_role("standard"))])
def get_private():
    return {"message": "Standard only"}
