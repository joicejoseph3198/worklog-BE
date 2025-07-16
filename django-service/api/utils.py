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
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Authorization header missing or invalid.")

        token = auth_header.split(" ")[1]

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
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")

