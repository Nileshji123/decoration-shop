from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from decor_app import views  # या जिस नाम से views import हैं

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('piyush-entry/', views.login, name='login'),
    path('piyush-dashbored/', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('booking/<int:pk>/', views.booking_page, name='booking_page'),
]

# Media aur Static files ko local server par chalane ke liye:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])