from django.contrib import admin
from django.urls import path
from salon_web import views
from django.conf import settings
from django.conf.urls.static import static
from .views import review_view, service_analysis
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # 🔑 Auth routes
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('profile/', views.profile, name='profile'),  # Profil sahifasi uchun yo'l
    path('profile/edit/',views.edit_profile, name='edit_profile'),
    path('get-available-times/', views.get_times_ajax, name='get_available_times'),
    path('review/', review_view, name='review'),
    path('analysis/', service_analysis, name='analysis'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('my-clients/', views.my_clients, name='my_clients'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('chat/', views.chatbot_response, name='chatbot'),  # Chatbot endpoint
    path('segments/', views.customer_segments, name='customer_segments'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
