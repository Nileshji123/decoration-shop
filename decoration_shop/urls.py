from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from decor_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. पब्लिक होमपेज (लाइव वेबसाइट)
    path('', views.home, name='home'),
    
    # 2. एडमिन लॉगिन
    path('piyush-entry/', views.login, name='login'),
    
    # 3. मेन डैशबोर्ड (कंट्रोल रूम)
    path('piyush-dashbored/', views.dashboard, name='dashboard'),
    
    # 4. इन्वेंटरी मैनेजमेंट (ऐड, डिलीट, लिस्टिंग)
    path('inventory/', views.inventory_view, name='inventory'),
    
    # 5. इन्वेंटरी अपडेट / एडिट पेज
    path('update-inventory/<int:pk>/', views.update_inventory_view, name='update_inventory'),
    
    # 6. स्टॉक मैनेजमेंट पेज
    path('stock/', views.stock_view, name='stock'),
    
    # 7. हिस्ट्री / रिकॉर्ड्स पेज
    path('history/', views.history_view, name='history'),
    
    # 8. यूजर डेटा / ग्राहक डिटेल्स पेज
    path('users/', views.users_view, name='users'),
    
    # 9. बुकिंग / डिटेल पेज (कस्टमर के लिए)
    path('booking/<int:pk>/', views.booking_page, name='booking_page'),

    # 10. पासवर्ड रिसेट और प्रोफाइल
    path('reset-admin-pwd-now/', views.reset_admin_password, name='reset_admin_password'),
    path('piyushprofile/', views.my_profile, name='my_profile'),
]

# 🔴 मीडिया फाइल्स का पाथ (अब यह रेंडर पर DEBUG=False होने पर भी काम करेगा)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# स्टैटिक फाइल्स सिर्फ लोकल (DEBUG = True) के लिए
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])