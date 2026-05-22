from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta
from .models import ThoiGianBieu
from .forms import ThoiGianBieuForm

# 1. Trang chủ hiển thị lịch tổng quát
def home(request):
    if request.user.is_authenticated:
        danh_sach_lich = ThoiGianBieu.objects.filter(
            sinh_vien=request.user, 
            thoi_gian__isnull=False
        ).order_by('thoi_gian')
    else:
        danh_sach_lich = []
    return render(request, 'schedule/home.html', {'lich': danh_sach_lich})

# 2. ĐĂNG NHẬP
def login_user(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('manage')
        else:
            error = "Tên đăng nhập hoặc mật khẩu không đúng!"
    return render(request, 'schedule/login.html', {'error': error})

# 3. ĐĂNG KÝ
def register(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        if p == u:
            error = "Mật khẩu không được giống tên đăng nhập!"
        elif u and p:
            try:
                user = User.objects.create_user(username=u, password=p)
                login(request, user)
                return redirect('manage')
            except:
                error = "Tên đăng nhập đã tồn tại!"
    return render(request, 'schedule/register.html', {'error': error})

# 4. ĐĂNG XUẤT
def logout_view(request):
    logout(request)
    return redirect('login') 

# 5. Dashboard quản lý cá nhân
@login_required(login_required_url='login')
def manage(request):
    if request.method == 'POST':
        form = ThoiGianBieuForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.sinh_vien = request.user
            new_item.save()
            return redirect('manage')
    else:
        form = ThoiGianBieuForm()
    
    items = ThoiGianBieu.objects.filter(sinh_vien=request.user).order_by('-id')
    return render(request, 'schedule/manage.html', {'lich': items, 'form': form})

# 6. Xóa môn học
@login_required(login_url='login')
def delete_lich(request, pk):
    item = get_object_or_404(ThoiGianBieu, pk=pk, sinh_vien=request.user)
    item.delete()
    return redirect('manage')

# 7. Gợi ý lịch THÔNG MINH (Sửa logic để khớp với hiển thị)
@login_required(login_url='login')
def auto_suggest(request):
    # Lấy các môn chưa có thời gian
    mon_chua_xep = ThoiGianBieu.objects.filter(
        sinh_vien=request.user, 
        thoi_gian__isnull=True
    ).order_by('do_kho') # Sắp xếp theo mức độ ưu tiên
    
    for item in mon_chua_xep:
        ngay = item.ngay_hoc if item.ngay_hoc else datetime.now().date()
        
        # MỐC GIỜ CHUẨN THEO ĐỘ KHÓ
        if item.do_kho == 'cao':
            gio_chuan = time(8, 0)   # Khó -> Học sáng (8h)
        elif item.do_kho == 'vua':
            gio_chuan = time(14, 0)  # Trung bình -> Học chiều (14h)
        else:
            gio_chuan = time(19, 0)  # Dễ -> Học tối (19h)
            
        thoi_gian_du_kien = datetime.combine(ngay, gio_chuan)
        
        # KIỂM TRA TRÙNG LỊCH TRONG NGÀY
        mon_da_co = ThoiGianBieu.objects.filter(
            sinh_vien=request.user,
            thoi_gian__date=ngay,
            thoi_gian__time__gte=gio_chuan
        ).order_by('thoi_gian').last()
        
        if mon_da_co and mon_da_co.thoi_gian:
            # Nếu đã có môn ở khung giờ này, xếp nối tiếp sau môn đó
            thoi_gian_du_kien = mon_da_co.thoi_gian + timedelta(hours=mon_da_co.thoi_luong)
            
        item.thoi_gian = thoi_gian_du_kien
        item.save()
        
    return redirect('home') # Sau khi xếp xong đẩy ra trang chủ xem kết quả