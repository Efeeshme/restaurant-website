from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def healthz(_request):
    return HttpResponse("ok", content_type="text/plain", status=200)

def sentry_test(_request):
    raise Exception("Sentry test error")


def trigger_error(request):
    division_by_zero = 1 / 0
    
urlpatterns = [
    path("healthz", healthz),
    path("sentry-test", sentry_test),  # <-- bunu ekle
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path('sentry-debug/', trigger_error),
]



