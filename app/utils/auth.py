import jwt

from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends, HTTPException, Request
from typing import Annotated
from jwt import PyJWKClient

from .config import (
    KEYCLOAK_AUTH_URL,
    KEYCLOAK_CERT_URL,
    KEYCLOAK_TOKEN_URL,
)

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=KEYCLOAK_TOKEN_URL,
    authorizationUrl=KEYCLOAK_AUTH_URL,
    refreshUrl=KEYCLOAK_TOKEN_URL,
)


async def valid_access_token(
    request: Request, access_token: Annotated[str, Depends(oauth_2_scheme)]
):
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
        request.state.user_data = data
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
