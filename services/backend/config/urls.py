from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/academic/", include("apps.academic.urls")),
    path("api/v1/attendance/", include("apps.attendance.urls")),
    path("api/v1/assignments/", include("apps.assignments.urls")),
    path("api/v1/activities/", include("apps.activities.urls")),
    path("api/v1/grants/", include("apps.grants.urls")),
    path("api/v1/penalties/", include("apps.penalties.urls")),
    path("api/v1/evaluations/", include("apps.evaluations.urls")),
    # API Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
