from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound


def spa_index(request):
    """Serve the compiled React SPA's index.html for all non-API routes.

    Asset URLs inside index.html point at /static/ (Vite base), which WhiteNoise
    serves from STATIC_ROOT after collectstatic.
    """
    index_file = Path(settings.FRONTEND_BUILD_DIR) / 'index.html'
    if index_file.exists():
        return HttpResponse(index_file.read_text(encoding='utf-8'))
    return HttpResponseNotFound(
        'Frontend build not found. Run "npm run build" in ./frontend, '
        'or use the Vite dev server (npm run dev) during local development.'
    )
