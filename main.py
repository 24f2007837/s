from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

app = FastAPI()

# --- Your Assigned Values ---
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

ALLOWED_ISSUER = "https://idp.exam.local"
ALLOWED_AUDIENCE = "tds-vpepzhkk.apps.exam.local"

# --- Request Schema ---
class TokenRequest(BaseModel):
    token: str

# --- Verify Endpoint ---
@app.post("/verify")
def verify_token(payload: TokenRequest):
    try:
        # PyJWT handles signature verification, expiry (exp), issuer (iss), and audience (aud) checks
        decoded_payload = jwt.decode(
            payload.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=ALLOWED_AUDIENCE,
            issuer=ALLOWED_ISSUER,
            options={"require": ["exp", "iss", "aud"]}
        )
        
        # On valid token, respond 200 with the echo of claims
        return {
            "valid": True,
            "email": decoded_payload.get("email"),
            "sub": decoded_payload.get("sub"),
            "aud": decoded_payload.get("aud")
        }

    except (ExpiredSignatureError, InvalidSignatureError, InvalidTokenError) as e:
        # On any validation failure, return a non-200 response (401 Unauthorized)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"valid": False}
        )