from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import User


class MongoUserWrapper:
    """Wraps a mongoengine User to satisfy DRF's request.user expectations."""

    def __init__(self, user: User):
        self._user = user
        self.id = str(user.id)
        self.email = user.email
        self.name = user.name
        self.role = user.role
        self.is_authenticated = True

    def __getattr__(self, item):
        return getattr(self._user, item)


class MongoJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        raw_token = auth_header.split(" ")[1]
        try:
            token = AccessToken(raw_token)
            user_id = token["user_id"]
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (MongoUserWrapper(user), None)
