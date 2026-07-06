from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from mongoengine.errors import NotUniqueError, ValidationError
from .models import User


def tokens_for_user(user: User):
    refresh = RefreshToken()
    refresh["user_id"] = str(user.id)
    refresh["role"] = user.role
    access = refresh.access_token
    access["user_id"] = str(user.id)
    access["role"] = user.role
    return {"access": str(access), "refresh": str(refresh)}


class RegisterView(APIView):
    """Patient self-registration. Staff accounts are seeded/created by admins."""

    def post(self, request):
        data = request.data
        required = ["email", "password", "name"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return Response(
                {"error": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User(
                email=data["email"],
                name=data["name"],
                phone=data.get("phone", ""),
                role="patient",
            )
            user.set_password(data["password"])
            user.save()
        except NotUniqueError:
            return Response({"error": "Email already registered"}, status=400)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {
                "user": {"id": str(user.id), "email": user.email, "name": user.name, "role": user.role},
                **tokens_for_user(user),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        return Response(
            {
                "user": {"id": str(user.id), "email": user.email, "name": user.name, "role": user.role},
                **tokens_for_user(user),
            }
        )
