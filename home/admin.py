from django.contrib import admin
from .models import SanPham, NhaCungCap, DanhMuc, KhachHang, NhanHieu, Category, CTHD,HoaDon

admin.site.register(SanPham)
admin.site.register(NhaCungCap)
admin.site.register(DanhMuc)
admin.site.register(KhachHang)
admin.site.register(NhanHieu)
admin.site.register(Category)
admin.site.register(CTHD)
admin.site.register(HoaDon)

# Register your models here.
class BlogAdminArea(admin.AdminSite):
    site_title = 'Thời trang trẻ em'
blog_site = BlogAdminArea(name='Blog Admin')