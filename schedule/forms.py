from django import forms  # Đã sửa lỗi chính tả 'foms' thành 'forms'
from .models import ThoiGianBieu

class ThoiGianBieuForm(forms.ModelForm):
    class Meta:
        model = ThoiGianBieu
        # Các trường này phải khớp với Model
        fields = ['ten_mon', 'do_kho', 'thoi_luong', 'ngay_hoc', 'phong_hoc']
        
        widgets = {
            'ten_mon': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ví dụ: Giải tích 1',
                'required': 'required'
            }),
            'do_kho': forms.Select(attrs={
                'class': 'form-select'
            }),
            'thoi_luong': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '10',
                'placeholder': 'Số giờ'
            }),
            'ngay_hoc': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'phong_hoc': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Phòng A101...'
            }),
        }

    # Tùy chỉnh nhãn hiển thị (nếu muốn ghi đè tên tiếng Việt)
    def __init__(self, *args, **kwargs):
        super(ThoiGianBieuForm, self).__init__(*args, **kwargs)
        self.fields['ten_mon'].label = "Tên môn học"
        self.fields['do_kho'].label = "Mức độ ưu tiên"
        self.fields['thoi_luong'].label = "Thời lượng (giờ)"
        self.fields['ngay_hoc'].label = "Ngày học"
        self.fields['phong_hoc'].label = "Địa điểm"