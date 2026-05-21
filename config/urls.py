"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from schedule import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import re

# Hàm tạo tài khoản admin nhanh
def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Đã tạo xong tài khoản! User: admin | Pass: admin123")
    return HttpResponse("Tài khoản admin đã tồn tại rồi!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:pk>/', views.delete_lich, name='delete_lich'),
    path('suggest/', views.auto_suggest, name='auto_suggest'),
    
    # Đường dẫn để kích hoạt tài khoản admin
    path('setup-admin/', create_admin),

    # --- CÁC ĐƯỜNG DẪN QUÊN MẬT KHẨU ---
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), 
         name="reset_password"),
    
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), 
         name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), 
         name="password_reset_complete"),
]

# --- ĐOẠN CODE QUAN TRỌNG ĐỂ HIỆN GIAO DIỆN TRÊN AZURE ---
if not settings.DEBUG:
    urlpatterns += [
        re_path(re.compile(r'^static/(?P<path>.*)$'), serve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)