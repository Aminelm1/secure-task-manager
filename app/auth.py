from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import httpx

security = HTTPBearer()

# URL utilisée par FastAPI à l'intérieur de Kubernetes
KEYCLOAK_INTERNAL_URL = "http://keycloak:8080"

REALM = "secure-task-manager"

# Issuer présent dans les tokens récupérés depuis localhost
# grâce au kubectl port-forward
KEYCLOAK_ISSUER = "http://localhost:8080/realms/secure-task-manager"

# FastAPI récupère les clés publiques directement auprès
# du service Keycloak à l'intérieur de Kubernetes
JWKS_URL = (
    f"{KEYCLOAK_INTERNAL_URL}/realms/{REALM}/"
    "protocol/openid-connect/certs"
)


def get_public_key(token: str):
    """
    Récupère la clé publique correspondant au token JWT.
    """

    try:
        header = jwt.get_unverified_header(token)

        response = httpx.get(
            JWKS_URL,
            timeout=10.0
        )
        response.raise_for_status()

        jwks = response.json()

        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                return key

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Public key not found"
        )

    except HTTPException:
        raise

    except Exception as e:
        print("JWKS ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to retrieve public key"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Vérifie le JWT envoyé dans :
    Authorization: Bearer <token>
    """

    token = credentials.credentials

    try:
        public_key = get_public_key(token)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            options={
                "verify_aud": False
            }
        )

        return payload

    except HTTPException:
        raise

    except Exception as e:
        # Important pour diagnostiquer les erreurs JWT
        print("JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def require_role(required_role: str):
    """
    Vérifie que l'utilisateur possède le rôle Keycloak demandé.
    """

    def role_checker(
        user=Depends(get_current_user)
    ):
        roles = user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )

        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )

        return user

    return role_checker