from django.db import models
from django.contrib.auth.models import User

class ThoiGianBieu(models.Model):
    sinh_vien = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name="Sinh viên"
    )
    ten_mon = models.CharField(max_length=200, verbose_name="Tên môn học")
    
    # 1. Đảm bảo Value ('cao', 'vua', 'thap') khớp 100% với logic trong views.py
    DO_KHO_CHOICES = [
        ('cao', 'Khó/Quan trọng (Sáng)'),
        ('vua', 'Trung bình (Chiều)'),
        ('thap', 'Dễ/Phụ (Tối)'),
    ]
    do_kho = models.CharField(
        max_length=10, 
        choices=DO_KHO_CHOICES, 
        default='vua', 
        verbose_name="Độ khó môn học"
    )
    
    thoi_luong = models.IntegerField(default=2, verbose_name="Số tiếng cần học (giờ)")
    ngay_hoc = models.DateField(null=True, blank=True, verbose_name="Ngày muốn học")
    
    # Trường thời gian bắt đầu
    thoi_gian = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Thời gian bắt đầu (Do máy gợi ý)"
    )
    
    phong_hoc = models.CharField(max_length=50, blank=True, verbose_name="Phòng học/Địa điểm")

    class Meta:
        verbose_name = "Lịch học"
        verbose_name_plural = "Danh sách lịch học"
        # Sắp xếp theo ngày học và thời gian bắt đầu
        ordering = ['ngay_hoc', 'thoi_gian']

    def __str__(self):
        return f"{self.ten_mon} ({self.get_do_kho_display()})"

    # --- HÀM BỔ SUNG ĐỂ FIX LỖI MÀU SẮC TRÊN GIAO DIỆN ---
    @property
    def get_badge_class(self):
        """Trả về class màu sắc của Bootstrap dựa trên độ khó thực tế"""
        if self.do_kho == 'cao':
            return 'danger'  # Màu đỏ
        elif self.do_kho == 'vua':
            return 'warning text-dark'  # Màu vàng
        else:
            return 'success'  # Màu xanh lá