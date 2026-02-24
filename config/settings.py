from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-key")

DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG


raw_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

raw_csrf = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in raw_csrf.split(",") if o.strip()]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "web.apps.WebConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local fallback (development only)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --------------------------------------------------
# MEDIA / STORAGE
# --------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

SUPABASE_S3_ENABLED = all(
    os.environ.get(k)
    for k in [
        "SUPABASE_S3_ACCESS_KEY_ID",
        "SUPABASE_S3_SECRET_ACCESS_KEY",
        "SUPABASE_S3_BUCKET",
        "SUPABASE_S3_REGION",
        "SUPABASE_S3_ENDPOINT_URL",
    ]
)

if SUPABASE_S3_ENABLED:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.environ["SUPABASE_S3_ACCESS_KEY_ID"],
                "secret_key": os.environ["SUPABASE_S3_SECRET_ACCESS_KEY"],
                "bucket_name": os.environ["SUPABASE_S3_BUCKET"],
                "region_name": os.environ["SUPABASE_S3_REGION"],
                "endpoint_url": os.environ["SUPABASE_S3_ENDPOINT_URL"],
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# --------------------------------------------------
# DEFAULT PK
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"