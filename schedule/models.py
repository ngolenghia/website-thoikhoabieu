from django.db import models
from django.contrib.auth.models import User

class ThoiGianBieu(models.Model):
    sinh_vien = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sinh viên")
    ten_mon = models.CharField(max_length=200, verbose_name="Tên môn học")
    
    # 1. Đảm bảo tên trường khớp với Logic suggest trong views.py
    DO_KHO_CHOICES = [
        ('cao', 'Khó/Quan trọng (Học sáng)'),
        ('vua', 'Trung bình (Học chiều)'),
        ('thap', 'Dễ/Phụ (Học tối)'),
    ]
    do_kho = models.CharField(max_length=10, choices=DO_KHO_CHOICES, default='vua', verbose_name="Độ khó môn học")
    thoi_luong = models.IntegerField(default=2, verbose_name="Số tiếng cần học (giờ)")
    ngay_hoc = models.DateField(null=True, blank=True, verbose_name="Ngày muốn học")
    
    # 2. Trường thời gian để máy tự điền (phải cho phép null để lúc đầu chưa có giờ không bị lỗi)
    thoi_gian = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian bắt đầu (Do máy gợi ý)")
    
    # 3. Đổi tên trường thành phong_hoc để đồng bộ với các thông báo lỗi trước đó
    phong_hoc = models.CharField(max_length=50, blank=True, verbose_name="Phòng học/Địa điểm")

    class Meta:
        verbose_name = "Lịch học"
        verbose_name_plural = "Danh sách lịch học"
        # Tự động sắp xếp môn học theo thời gian sớm nhất lên đầu
        ordering = ['thoi_gian']

    def __str__(self):
        # Hiển thị tên môn kèm độ khó trong trang Admin cho dễ nhìn
        return f"{self.ten_mon} ({self.get_do_kho_display()})"