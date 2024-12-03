

from django.urls import path
from .views import CustomLoginView  # Import your custom login view
from . import views  # Import other views from the same app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='text'),  # Assuming 'home' is defined in views.py
    path('registration/', views.registration, name='registration'),  # Registration page
    path('login/', CustomLoginView.as_view(), name='login'),  # Use as_view() for class-based views
]

# Include media files handling when in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]
