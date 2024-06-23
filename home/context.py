from .models import GioHang, KhachHang, Category, DanhMuc

def demGioHang(request):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = KhachHang.objects.get(maKH=maKH)
        so_luong = GioHang.objects.filter(maKH=khachHang).count()
    else:
        so_luong = 0
    return {"demGioHang": so_luong}

def category_danhmuc(request):
    category_list = Category.objects.all()
    danhmuc_list = DanhMuc.objects.all()
    return {
        'category_list': category_list,
        'danhmuc_list': danhmuc_list,
    }
