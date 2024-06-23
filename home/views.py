from django.http import HttpResponseRedirect, HttpResponse, request
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    SanPham,
    KichCo,
    DanhMuc,
    HoaDon,
    Category,
    CTHD,
    TinhTrangDonHang,
    QLSP,
    KhachHang,
    GioHang,
    YeuThich,
    Review,
)
from django.core.paginator import Paginator
from .forms import (
    KhachHangLoginForm,
    KhachHangForm,
    KhachHangRegistrationForm,
    ChangePasswordForm,
    ReviewForm,
)
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import hashlib
import hmac
import time
import os
from urllib.parse import urlencode
import datetime
from django.contrib import messages

from django.db.models import Sum
import random


def index(request):
    sanpham_list = SanPham.objects.all()
    danhMuc_list = DanhMuc.objects.all()
    category_list = Category.objects.all()
    return render(
        request,
        "page/home.html",
        {
            "sanpham_list": sanpham_list,
            "danhmuc_list": danhMuc_list,
            "category_list": category_list,
        },
    )


def category_list(request):
    category_list = Category.objects.all()
    return render(request, "page/home.html", {"category_list": category_list})


def sanpham_list(request):
    sanpham_list = SanPham.objects.all()
    paginator = Paginator(sanpham_list, 8)
    soTrang = request.GET.get("page")
    trang = paginator.get_page(soTrang)

    return render(request, "page/DSSanPham.html", {"sanpham_list": trang})


def danhMuc_list(request):
    danhmuc_list = DanhMuc.objects.all()
    return render(request, "page/home.html", {"danhmuc_list": danhmuc_list})


def search(request):
    sanpham_list_search = None
    if "s" in request.GET:
        s = request.GET["s"].strip()
        if s:
            sanpham_list_search = SanPham.objects.filter(tenSP__icontains=s)
    return render(
        request, "page/search.html", {"sanpham_list_search": sanpham_list_search}
    )


def chiTietSP(request, maSP):
    san_pham = get_object_or_404(SanPham, maSP=maSP)
    kichCo = san_pham.kichCo.all().order_by("-maSize")
    qlsp = get_object_or_404(QLSP, maSP=san_pham)
    is_favorite = False
    danhGia = Review.objects.filter(maSP=san_pham)

    maKH = request.session.get("khach_hang_id")
    khachHang = None
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        is_favorite = YeuThich.objects.filter(maKH=khachHang, maSP=san_pham).exists()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            danh_gia = review_form.save(commit=False)
            danh_gia.maKH = khachHang
            danh_gia.maSP = san_pham
            danh_gia.save()
            return redirect("chi-tiet-san-pham", maSP=maSP)
    else:
        review_form = ReviewForm()
    sanpham_list = list(SanPham.objects.all())
    random_sanpham_list = random.sample(sanpham_list, 3)
    data = {
        "san_pham": san_pham,
        "kichCo": kichCo,
        "qlsp": qlsp,
        "is_favorite": is_favorite,
        "ReviewForm": review_form,
        "danhGia": danhGia,
        "sanpham_list": random_sanpham_list,
    }
    return render(request, "page/ChiTietSP.html", data)


def DSSP_theoLoai(request, tenL):
    san_pham_theo_loai = SanPham.objects.filter()


def login(request):
    errors = []
    if request.method == "POST":
        form = KhachHangLoginForm(request.POST)
        if form.is_valid():
            tenDN = form.cleaned_data.get("tenDN")
            matKhau = form.cleaned_data.get("matKhau")
            try:
                khach_hang = KhachHang.objects.get(tenDN=tenDN)
                if khach_hang.matKhau == matKhau:
                    request.session["khach_hang_id"] = khach_hang.maKH
                    return redirect("index")
                else:
                    errors.append("Tên đăng nhập hoặc mật khẩu không đúng")
            except KhachHang.DoesNotExist:
                errors.append("Tên đăng nhập hoặc mật khẩu không đúng")
    else:
        form = KhachHangLoginForm()

    return render(request, "page/login.html", {"form": form, "errors": errors})


def logout(request):
    if "khach_hang_id" in request.session:
        del request.session["khach_hang_id"]
    return redirect("index")


def register(request):
    errors = None
    if request.method == "POST":
        form = KhachHangRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            errors = form.errors
    else:
        form = KhachHangRegistrationForm()
    return render(request, "page/register.html", {"form": form, "errors": errors})


def addYeuThich(request, maSP):
    if request.method == "POST":
        san_pham = get_object_or_404(SanPham, maSP=maSP)
        maKH = request.session.get("khach_hang_id")
        url = request.POST.get("next", "/")

        if maKH:
            khachHang = get_object_or_404(KhachHang, maKH=maKH)
            yeuThich, created = YeuThich.objects.get_or_create(
                maKH=khachHang,
                maSP=san_pham,
            )
            if not created:
                yeuThich.delete()
            else:
                yeuThich.save()

        return redirect(url)


def xemYeuThich(request):
    maKH = request.session.get("khach_hang_id")

    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        xemYeuThich = YeuThich.objects.filter(maKH=khachHang)
    else:
        xemYeuThich = []

    data = {
        "xemYeuThich": xemYeuThich,
    }
    return render(request, "page/yeuThich.html", data)


def addGioHang(request, maSP):
    if request.method == "POST":
        san_pham = get_object_or_404(SanPham, maSP=maSP)
        maKH = request.session.get("khach_hang_id")
        chonSize = request.POST.get("kichCo")

        url = request.POST.get("next", "/")

        if maKH:
            khachHang = KhachHang.objects.get(maKH=maKH)
            soLuong = int(request.POST.get("soLuong", 1))
            gioHang, created = GioHang.objects.get_or_create(
                maKH=khachHang,
                maSP=san_pham,
                kichCo=chonSize,
                defaults={"soLuong": soLuong, "donGia": san_pham.giaBan},
            )
            if not created:
                gioHang.soLuong += soLuong
                gioHang.save()

        return redirect(url)


def xemGioHang(request):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        gioHang_items = GioHang.objects.filter(maKH=khachHang)
    else:
        gioHang_items = []
    gioHang_thanhTien = []
    tongTien = 0

    for item in gioHang_items:
        san_pham = get_object_or_404(SanPham, maSP=item.maSP.maSP)
        thanhTien = item.soLuong * san_pham.giaBan
        gioHang_thanhTien.append(
            {
                "item": item,
                "thanhTien": thanhTien,
                "tenSP": san_pham.tenSP,
                "mauSac": san_pham.mauSac,
                "kichCo": item.kichCo,
                "hinhAnh": san_pham.hinhanh.url if san_pham.hinhanh else "",
            }
        )
        tongTien += thanhTien
    sanpham_list = list(SanPham.objects.all())
    random_sanpham_list = random.sample(sanpham_list, 3)
    data = {
        "gioHang_thanhTien": gioHang_thanhTien,
        "tongTien": tongTien,
        "sanpham_list": random_sanpham_list,
    }
    return render(request, "page/gioHang.html", data)


def xoaSPGioHang(request, maSP, maSize):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        gioHang_item = get_object_or_404(
            GioHang, maKH=khachHang, maSP=maSP, kichCo=maSize
        )
        gioHang_item.delete()
        return redirect("xemGioHang")
    else:
        return redirect("login")


def xoaTatCaGioHang(request):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        GioHang.objects.filter(maKH=khachHang).delete()

        return redirect("xemGioHang")
    else:
        return redirect("login")


def SPTheoDM(request, maDM):
    dm = get_object_or_404(DanhMuc, maDM=maDM)
    spdm = SanPham.objects.filter(maDM=dm)
    sanpham_list = list(SanPham.objects.all())
    random_sanpham_list = random.sample(sanpham_list, 3)
    return render(
        request,
        "page/DSSP_TheoLoai.html",
        {"dm": dm, "spdm": spdm, "sanpham_list": random_sanpham_list},
    )


def SPTheoCate(request, maCate):
    cate = get_object_or_404(Category, maCate=maCate)
    spc = SanPham.objects.filter(maCate=cate)
    return render(request, "page/DSSanPham.html", {"cate": cate, "spc": spc})


@require_POST
def capNhatGioHang(request):
    data = json.loads(request.body)
    maSP = data.get("maSP")
    soLuong = data.get("soLuong")
    maKH = request.session.get("khach_hang_id")

    if maKH and maSP and soLuong:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        sanPham = get_object_or_404(SanPham, maSP=maSP)
        gioHang_item = get_object_or_404(GioHang, maKH=khachHang, maSP=sanPham)

        gioHang_item.soLuong = int(soLuong)
        gioHang_item.save()

        gioHang_items = GioHang.objects.filter(maKH=khachHang)
        tongTien = sum(item.soLuong * item.donGia for item in gioHang_items)
        thanhTien = gioHang_item.soLuong * gioHang_item.donGia

        return JsonResponse(
            {"success": True, "thanhTien": thanhTien, "tongTien": tongTien}
        )
    return JsonResponse({"success": False}, status=400)


def thanhToan(request):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        gioHang_items = GioHang.objects.filter(maKH=khachHang)

        if request.method == "POST":
            pttt = request.POST.get("pttt")
            if pttt == "momo":
                datHang_id = str(int(time.time()))
                tong = sum(item.soLuong * item.donGia for item in gioHang_items)
                thongTinDatHang = "Thanh toán đơn hàng {}".format(datHang_id)
                thanhToan_url = thanhToanMomo(datHang_id, tong, thongTinDatHang)
                return redirect(thanhToan_url)
            elif pttt == "cash":
                tinh_trang_tt = TinhTrangDonHang.objects.get(maTT="DH")
                hoa_don = HoaDon.objects.create(
                    maKH=khachHang,
                    ngayDatHang=datetime.datetime.now(),
                    tongTien=sum(item.soLuong * item.donGia for item in gioHang_items),
                    tinhTrang=tinh_trang_tt,
                    phuongThucThanhToan="Tiền mặt",
                )
                for item in gioHang_items:
                    CTHD.objects.create(
                        maHD=hoa_don,
                        maSP=item.maSP,
                        soLuong=item.soLuong,
                        donGiaBan=item.donGia,
                        thanhTien=item.soLuong * item.donGia,
                    )
                GioHang.objects.filter(maKH=khachHang).delete()

                messages.success(request, "Thanh toán thành công!")
                return redirect("thanhToanThanhCong")

        gioHang_thanhTien = []
        tongTien = 0

        for item in gioHang_items:
            thanhTien = item.soLuong * item.donGia
            san_pham = item.maSP
            gioHang_thanhTien.append(
                {
                    "item": item,
                    "thanhTien": thanhTien,
                    "tenSP": san_pham.tenSP,
                    "mauSac": san_pham.mauSac,
                    "kichCo": item.kichCo,
                    "hinhAnh": san_pham.hinhanh.url if san_pham.hinhanh else "",
                }
            )
            tongTien += thanhTien
        sanpham_list = list(SanPham.objects.all())
        random_sanpham_list = random.sample(sanpham_list, 3)
        data = {
            "gioHang_thanhTien": gioHang_thanhTien,
            "tongTien": tongTien,
            "khachHang": khachHang,
            "sanpham_list": random_sanpham_list,
        }
        return render(request, "page/thanhToan.html", data)
    else:
        return redirect("login")


def thanhToanMomo(datHang_id, tong, thongTinDatHang):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partner_code = "MOMOBKUN20180529"
    access_key = "klm05TvNBzhg7h7j"
    secret_key = "at67qH6mk8w5Y1nAyMoYKMWACiEi2bsa"
    return_url = "http://localhost:8000/thanhToan_return"
    notify_url = "http://localhost:8000/thanhToan_thongbao"

    request_id = str(int(time.time()))
    tong = str(tong)
    raw_signature = f"accessKey={access_key}&tong={tong}&extraData=&ipnUrl={notify_url}&orderId={datHang_id}&orderInfo={thongTinDatHang}&partnerCode={partner_code}&redirectUrl={return_url}&requestId={request_id}&requestType=captureMoMoWallet"

    signature = hmac.new(
        bytes(secret_key, "utf-8"), bytes(raw_signature, "utf-8"), hashlib.sha256
    ).hexdigest()

    data = {
        "partnerCode": partner_code,
        "accessKey": access_key,
        "requestId": request_id,
        "tong": tong,
        "orderId": datHang_id,
        "orderInfo": thongTinDatHang,
        "returnUrl": return_url,
        "notifyUrl": notify_url,
        "extraData": "",
        "requestType": "captureMoMoWallet",
        "signature": signature,
        "lang": "vi",
    }

    response = request.post(endpoint, json=data)
    response_data = response.json()

    if "payUrl" in response_data:
        return response_data["payUrl"]
    else:
        raise Exception(
            "MoMo API response does not contain 'payUrl'. Response: {}".format(
                response_data
            )
        )


def thanhToan_return(request):
    if request.method == "GET":
        data = request.GET
        if data.get("errorCode") == "0":
            maKH = request.session.get("khach_hang_id")
            if maKH:
                khachHang = get_object_or_404(KhachHang, maKH=maKH)
                gioHang_items = GioHang.objects.filter(maKH=khachHang)
                tinh_trang_tt = TinhTrangDonHang.objects.get(maTT="DH")
                hoa_don = HoaDon.objects.create(
                    maKH=khachHang,
                    ngayDatHang=datetime.datetime.now(),
                    tongTien=sum(item.soLuong * item.donGia for item in gioHang_items),
                    tinhTrang=tinh_trang_tt,
                    phuongThucThanhToan="MoMo",
                )
                for item in gioHang_items:
                    CTHD.objects.create(
                        maHD=hoa_don,
                        maSP=item.maSP,
                        soLuong=item.soLuong,
                        donGiaBan=item.donGia,
                        thanhTien=item.soLuong * item.donGia,
                    )
                GioHang.objects.filter(maKH=khachHang).delete()
                return redirect("thanhToanThanhCong")
    return HttpResponse("Payment failed or cancelled")


def thanhToan_thongbao(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data["errorCode"] == "0":
            datHang_id = data["orderId"]
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def thanhToanThanhCong(request):
    sanpham_list = list(SanPham.objects.all())
    random_sanpham_list = random.sample(sanpham_list, 3)
    data = {
        "sanpham_list": random_sanpham_list,
    }
    return render(request, "page/thanhToanThanhCong.html", data)


def xemDonHang(request):
    maKH = request.session.get("khach_hang_id")
    if maKH:
        khachHang = get_object_or_404(KhachHang, maKH=maKH)
        hoa_don_list = HoaDon.objects.filter(maKH=khachHang).order_by("-ngayDatHang")

        chitietdathang = []
        for hoa_don in hoa_don_list:
            cthd_list = CTHD.objects.filter(maHD=hoa_don)
            chitietdathang.append({"hoa_don": hoa_don, "cthd_list": cthd_list})

        data = {"chitietdathang": chitietdathang}
        return render(request, "page/xemDonHang.html", data)
    else:
        return redirect("login")


def xemThongTinKhachHang(request):
    maKH = request.session.get("khach_hang_id")
    khachHang = get_object_or_404(KhachHang, maKH=maKH)

    form = KhachHangForm(instance=khachHang)
    password_form = ChangePasswordForm()

    if request.method == "POST":
        if "infoForm" in request.POST:
            form = KhachHangForm(request.POST, instance=khachHang)
            if form.is_valid():
                form.save()
                messages.success(request, "Thông tin đã được lưu thành công!")
                return redirect("xemThongTinKhachHang")
            else:
                messages.error(request, "Có lỗi xảy ra khi lưu thông tin.")

        elif "passwordForm" in request.POST:
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data["old_password"]
                if check_password(old_password, khachHang.matKhau):
                    new_password = password_form.cleaned_data["new_password"]
                    khachHang.matKhau = make_password(new_password)
                    khachHang.save()
                    messages.success(request, "Mật khẩu đã được thay đổi thành công!")
                    return redirect("xemThongTinKhachHang")
                else:
                    password_form.add_error(
                        "old_password", "Mật khẩu cũ không chính xác."
                    )
            else:
                messages.error(request, "Có lỗi xảy ra khi thay đổi mật khẩu.")

    return render(
        request,
        "page/thongTinKhachHang.html",
        {"form": form, "password_form": password_form},
    )
