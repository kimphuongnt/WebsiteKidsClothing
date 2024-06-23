from django.urls import path
from . import views  # call to url_shortener/views.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("danh-sach-san-pham/", views.sanpham_list, name="sanpham_list"),
    path("chi-tiet-san-pham/<str:maSP>/", views.chiTietSP, name="chi-tiet-san-pham"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("search/", views.search, name="search"),
    path("gio-hang/", views.xemGioHang, name="xemGioHang"),
    path("them-vao-gio-hang/<str:maSP>/", views.addGioHang, name="addGioHang"),
    path("them-yeu-thich/<str:maSP>/", views.addYeuThich, name="addYeuThich"),
    path("yeu-thich/", views.xemYeuThich, name="xemYeuThich"),
    path(
        "gio-hang-xoa/<str:maSP>/<str:maSize>/", views.xoaSPGioHang, name="xoaSPGioHang"
    ),
    path("xoa-tat-ca-gio-hang/", views.xoaTatCaGioHang, name="xoaTatCaGioHang"),
    path("danh-muc/<str:maDM>/", views.SPTheoDM, name="SPTheoDM"),
    path("gio-hang/cap-nhat/", views.capNhatGioHang, name="capNhatGioHang"),
    path("thanh-toan/", views.thanhToan, name="thanhToan"),
    path("thanh-toan-thanh-cong/", views.thanhToanThanhCong, name="thanhToanThanhCong"),
    path("thanhToan_return/", views.thanhToan_return, name="thanhToan_return"),
    path("thanhToan_thongbao/", views.thanhToan_thongbao, name="thanhToan_thongbao"),
    path("xem-don-hang/", views.xemDonHang, name="xemDonHang"),
    path(
        "thong-tin-khach-hang/", views.xemThongTinKhachHang, name="xemThongTinKhachHang"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
