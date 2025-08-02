import jwt
import time
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import PyJWKClient
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    """
        DRF will call that class’s .authenticate(self, request) method to try to identify and authenticate the user.
        You can handle different token formats or headers inside this method.
        """
    def authenticate(self, request):
        start_time = time.time()
        auth_header = request.headers.get('Authorization')
        
        # For development, allow requests without authentication
        # if not auth_header:
        #     Return a default user for development
        #     return None, {"sub": "dev-user-123", "token": None}
        
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Authorization header missing or invalid.")

        token = auth_header.split(" ")[1]

        # For development, if we have a token but can't verify it, still allow the request
        try:
            # Decode and verify
            payload = jwt.decode(
                token,
                settings.JWKS_PUBLIC_KEY,
                algorithms=["RS256"],
                options={"verify_aud": False},
                leeway=10
            )

            subject = payload.get("sub")
            if not subject:
                raise AuthenticationFailed("Token missing 'sub' claim.")
            duration = time.time() - start_time
            print(f"[JWTAuthentication] Token verification took {duration:.4f} seconds.")
            return None, {"sub": subject, "token": token}
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired.")
        except (jwt.InvalidTokenError, jwt.InvalidKeyError) as e:
            # For development, if token verification fails, still allow with default user
            print(f"[JWTAuthentication] Token verification failed: {str(e)}. Using default user for development.")
            return None, {"sub": "dev-user-123", "token": token}

