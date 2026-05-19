"""Auth router - admin login endpoint."""

import logging
from fastapi import APIRouter, HTTPException, Request, status

from app.auth import create_access_token
from app.config import ADMIN_PASSWORD, ADMIN_USERNAME
from app.schemas import TokenResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def admin_login(request: Request):
    try:
        content_type = request.headers.get("content-type", "").lower()

        if "application/json" in content_type:
            payload = await request.json()
            username = payload.get("username", "")
            password = payload.get("password", "")
        else:
            form = await request.form()
            username = str(form.get("username", ""))
            password = str(form.get("password", ""))

        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            logger.warning(f"Failed login attempt for username: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        token = create_access_token(data={"sub": username})
        logger.info(f"Successful login for username: {username}")
        return TokenResponse(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )
