import jwt

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
from typing import Annotated

from utils.config import (
    KEYCLOAK_TOKEN_URL,
    KEYCLOAK_AUTH_URL,
    KEYCLOAK_CERT_URL,
)

app = FastAPI()

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=KEYCLOAK_TOKEN_URL,
    authorizationUrl=KEYCLOAK_AUTH_URL,
    refreshUrl=KEYCLOAK_TOKEN_URL,
)


async def valid_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = KEYCLOAK_CERT_URL
    jwks_client = PyJWKClient(url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="account",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=498, detail="Token has expired")
    except Exception as e:
        print("An exception occurred: ", e)
        raise HTTPException(status_code=401, detail="Invalid Authorization")


def has_role(role_name: str):
    async def check_role(token_data: Annotated[dict, Depends(valid_access_token)]):
        roles = token_data["resource_access"]["nextjs"]["roles"]
        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


@app.get("/public")
def get_public():
    return {"message": "PUBLIC ROUTE"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "PRIVATE ROUTE"}


@app.get("/admin", dependencies=[Depends(has_role("admin"))])
def get_private():
    return {"message": "Admin only"}


@app.get("/standard", dependencies=[Depends(has_role("standard"))])
def get_private():
    return {"message": "Standard only"}
