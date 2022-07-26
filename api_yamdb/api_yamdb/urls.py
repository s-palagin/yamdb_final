from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

api_patterns = [
    path('', include('users.urls')),
    path('', include('api.urls')),
]

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
