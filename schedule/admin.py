from django.contrib import admin
from .models import ThoiGianBieu

#admin.site.register(ThoiGianBieu)from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# 1. Định nghĩa lớp quản lý User tùy chỉnh
class CustomUserAdmin(UserAdmin):
    # Hàm này dùng để ẩn/hiện các ô nhập liệu
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Nếu không phải là "Trùm cuối" (Superuser), ta ẩn ô mật khẩu
        if not request.user.is_superuser:
            fields = list(fields)
            if 'password' in fields:
                fields.remove('password')
        return fields

    # Hàm này chặn quyền thay đổi mật khẩu trực tiếp trong Admin
    def has_change_permission(self, request, obj=None):
        # Nếu đang xem một User cụ thể và không phải Superuser thì chặn
        if obj and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

# 2. Gỡ bỏ cách quản lý User mặc định của Django
admin.site.unregister(User)

# 3. Đăng ký lại User với cách quản lý "An toàn" mới của bạn
admin.site.register(User, CustomUserAdmin)

# 4. Đăng ký lại bảng ThoiGianBieu của bạn (nhớ bỏ dấu # ở đầu)
from .models import ThoiGianBieu
admin.site.register(ThoiGianBieu)