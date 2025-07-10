import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    """
    DRF will call that class’s .authenticate(self, request) method to try to identify and authenticate the user.
    You can handle different token formats or headers inside this method.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startsWith('Bearer '):
            raise AuthenticationFailed("Authorization header not found or invalid.")

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            subject = payload.get("sub")
            if not subject:
                raise AuthenticationFailed('Token missing key details')
            return None, {"sub": subject, "token": token}
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
