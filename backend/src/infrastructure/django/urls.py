from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from src.infrastructure.django.views import (
    AnalysisViewSet,
    DatasetViewSet,
    LoginView,
    ProjectViewSet,
)

# Create the router
router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"datasets", DatasetViewSet)
router.register(r"analyses", AnalysisViewSet)

urlpatterns = [
    # Redirect root URL to API
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/login", LoginView.as_view(), name="login"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
