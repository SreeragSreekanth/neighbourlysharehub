from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static  # Import the static helper function


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userauth.urls')),
    path('', include('user.urls')),
    path('', include('Admin.urls')),
    path('', include('itemlisting.urls')),
    path('', include('itemlisting.urls')),
    path('', include('category_management.urls')),

    ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

