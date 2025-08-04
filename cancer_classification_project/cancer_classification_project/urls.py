from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# Optional: Simple homepage
def home(request):
    return HttpResponse("<h1>Welcome to the Cancer Classification API</h1><p>Use /predict/ to classify cancer subtypes.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('classification.urls')),  # ✅ All your /api/... endpoints come from here
]

# ✅ Serve SHAP plots from media during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
