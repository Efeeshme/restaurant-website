from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def healthz(_request):
    return HttpResponse("ok", content_type="text/plain", status=200)

urlpatterns = [
    path("healthz", healthz),          # <-- Koyeb health check buraya
    path("admin/", admin.site.urls),
    path("", include("web.urls")),     # senin mevcut site route’ların
]