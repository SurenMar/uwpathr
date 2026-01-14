from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings

def health_check(request):
  return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('health/', health_check),
    path('api/', include('users.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/', include('checklists.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('progress.urls')),
]

if settings.DEVELOPMENT_MODE:
  urlpatterns.insert(0, path('admin/', admin.site.urls))