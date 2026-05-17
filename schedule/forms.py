from django import forms
from .models import ThoiGianBieu

class ThoiGianBieuForm(forms.ModelForm):
    class Meta:
        model = ThoiGianBieu
        fields = ['ten_mon', 'do_kho', 'thoi_luong', 'ngay_hoc', 'phong_hoc']
        widgets = {
            'ten_mon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Giải tích 1'}),
            'do_kho': forms.Select(attrs={'class': 'form-select'}),
            'thoi_luong': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'ngay_hoc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phong_hoc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phòng A101...'}),
        }