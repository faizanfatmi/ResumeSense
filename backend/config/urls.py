from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from config.views import spa_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/files/', include('apps.documents.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    path('api/job-matcher/', include('apps.jobmatcher.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/reports/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve the React SPA for everything else (client-side routing). Kept last so it
# never shadows the API or admin routes above.
urlpatterns += [
    re_path(r'^(?!api/|admin/|static/|media/).*$', spa_index),
]
