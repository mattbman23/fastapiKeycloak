from dotenv import load_dotenv
import os

load_dotenv()

KEYCLOAK_TOKEN_URL = os.getenv("KEYCLOAK_TOKEN_URL")
KEYCLOAK_AUTH_URL = os.getenv("KEYCLOAK_AUTH_URL")
KEYCLOAK_CERT_URL = os.getenv("KEYCLOAK_CERT_URL")
