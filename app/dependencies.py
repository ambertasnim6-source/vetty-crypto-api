import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings


security = HTTPBearer()


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    settings = get_settings()

    if not secrets.compare_digest(
        credentials.credentials,
        settings.api_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return credentials.credentials