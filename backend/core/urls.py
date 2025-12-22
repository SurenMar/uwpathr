from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('checklists.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('progress.urls')),
]
