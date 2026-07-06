import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import mongoengine

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts",
    "doctors",
    "services",
    "enquiries",
    "bookings",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "clinic_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "clinic_backend.wsgi.application"

# No relational DB used for app data — mongoengine handles MongoDB directly.
# A minimal SQLite DB is configured only to satisfy Django's internal
# framework requirements (django.contrib.auth/contenttypes imports).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django_framework.sqlite3",
    }
}

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/devs_clinic")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "devs_clinic")
mongoengine.connect(host=MONGO_URI, db=MONGO_DB_NAME, alias="default")

AUTH_USER_MODEL = "auth.User"  # Django's built-in auth is unused for app logic;
# our real user data lives in accounts.models.User (mongoengine). This is only
# present to satisfy django.contrib.auth's internal requirements.

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.MongoJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000"
).split(",")

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Email notifications (enquiry/booking alerts) ---
# Uses Resend's SMTP relay (https://resend.com). EMAIL_HOST_USER is always the
# literal string "resend"; EMAIL_HOST_PASSWORD is your Resend API key.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.resend.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "resend")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "onboarding@resend.dev")
CLINIC_NOTIFICATION_EMAIL = os.getenv("CLINIC_NOTIFICATION_EMAIL", "mdhivakar091@gmail.com")

# If no API key is set, fall back to printing emails to the console instead of
# crashing — useful for local dev before Resend is configured.
if not EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
