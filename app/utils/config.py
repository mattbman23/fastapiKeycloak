from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
KEYCLOAK_TOKEN_URL = os.getenv("KEYCLOAK_TOKEN_URL")
KEYCLOAK_AUTH_URL = os.getenv("KEYCLOAK_AUTH_URL")
KEYCLOAK_CERT_URL = os.getenv("KEYCLOAK_CERT_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
WX_API_KEY = os.environ.get("WX_API_KEY")
WX_PROJECT_ID = os.environ.get("WX_PROJECT_ID")
WX_URL = os.environ.get("WX_URL")
