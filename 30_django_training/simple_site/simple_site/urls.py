from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('', include('root_app.urls')),
    path('admin/', admin.site.urls),
    re_path('styled_app/', include('styled_app.urls')),
    re_path('news/', include('news.urls')),
]
