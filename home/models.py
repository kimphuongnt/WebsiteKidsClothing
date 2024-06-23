from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Category(models.Model):
    maCate = models.CharField(max_length=20, primary_key=True)
    tenCate = models.TextField()

    def __str__(self):
        return self.tenCate


class DanhMuc(models.Model):
    maDM = models.CharField(max_length=20, primary_key=True)
    tenDM = models.TextField()
    maCate = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.tenDM


class NhanHieu(models.Model):
    maNH = models.CharField(max_length=20, primary_key=True)
    tenNH = models.TextField()
    xuatXu = models.TextField()

    def __str__(self):
        return self.tenNH


class NhaCungCap(models.Model):
    maNCC = models.CharField(max_length=20, primary_key=True)
    tenNCC = models.TextField()
    diaChi = models.TextField()
    soDT = models.CharField(max_length=15)
    eMail = models.EmailField(max_length=50)

    def __str__(self):
        return self.maNCC + " " + self.tenNCC


class PhieuNhap(models.Model):
    maPN = models.AutoField(primary_key=True)
    ngayNhap = models.DateField()
    maNCC = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE)


class KichCo(models.Model):
    maSize = models.CharField(max_length=5, primary_key=True)
    tenSize = models.CharField(max_length=10)

    def __str__(self):
        return self.tenSize


class SanPham(models.Model):
    NAM = "NAM"
    NU = "NU"
    UNISEX = "UNISEX"
    GIOI_TINH = [
        (NAM, "Nam"),
        (NU, "Nữ"),
        (UNISEX, "Unisex"),
    ]

    maSP = models.CharField(max_length=20, primary_key=True)
    tenSP = models.TextField()
    moTa = models.TextField()
    giaBan = models.IntegerField()
    chatLieu = models.TextField()
    mauSac = models.TextField()
    gioiTinh = models.CharField(
        max_length=6,
        choices=GIOI_TINH,
        default=UNISEX,
    )
    maDM = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)
    maNH = models.ForeignKey(NhanHieu, on_delete=models.CASCADE)
    maNCC = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE)
    hinhanh = models.ImageField(null=True, upload_to="images/sanpham/")
    hinhanh1 = models.ImageField(null=True, upload_to="images/sanpham/")
    kichCo = models.ManyToManyField(KichCo)

    def __str__(self):
        return self.maSP + " " + self.tenSP


class CTPN(models.Model):
    maPN = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE)
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    soLuongNhap = models.IntegerField(default=0)
    donGiaNhap = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["maPN", "maSP"], name="unique_maPN_maSP")
        ]


class KhachHang(models.Model):
    maKH = models.AutoField(primary_key=True)
    tenKH = models.TextField()
    soDT = models.CharField(max_length=15)
    eMail = models.EmailField(max_length=50)
    diaChi = models.TextField()
    gioiTinh = models.TextField()
    tenDN = models.CharField(max_length=50)
    matKhau = models.CharField(max_length=50)

    def __str__(self):
        return self.tenKH


class TinhTrangDonHang(models.Model):
    maTT = models.CharField(max_length=2, primary_key=True)
    tenTT = models.CharField(max_length=50)

    def __str__(self):
        return self.tenTT


class HoaDon(models.Model):
    maHD = models.AutoField(primary_key=True)
    maKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    ngayDatHang = models.DateField()
    tongTien = models.IntegerField(default=0)
    tinhTrang = models.ForeignKey(TinhTrangDonHang, on_delete=models.CASCADE)
    phuongThucThanhToan = models.CharField(max_length=50, default="Tiền mặt")

    def __str__(self):
        return f"Hóa đơn {self.maHD} - {self.maKH.tenKH}"


class CTHD(models.Model):
    maHD = models.ForeignKey(HoaDon, on_delete=models.CASCADE)
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    kichCo = models.CharField(max_length=10, default="S")
    soLuong = models.IntegerField(default=0)
    donGiaBan = models.IntegerField(default=0)
    thanhTien = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.maHD}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["maHD", "maSP"], name="unique_maHD_maSP")
        ]


class QLSP(models.Model):
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    soLuongNhap = models.IntegerField(default=0)
    soLuongXuat = models.IntegerField(default=0)
    soLuongTonKho = models.IntegerField(default=0)


class GioHang(models.Model):
    maKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    soLuong = models.IntegerField()
    donGia = models.IntegerField()
    kichCo = models.CharField(max_length=10)
    tongTien = models.IntegerField()

    def save(self, *args, **kwargs):
        self.tongTien = self.soLuong * self.donGia
        super(GioHang, self).save(*args, **kwargs)


class YeuThich(models.Model):
    maKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("maKH", "maSP")

    def __str__(self):
        return f"{self.maKH} yêu thích {self.maSP}"


class Review(models.Model):
    maKH = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    maSP = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    diemDanhGia = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    danhGia = models.TextField(blank=True, null=True)
    ngayDanhGia = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.maSP} - {self.maKH} - {self.diemDanhGia}"


@receiver(post_save, sender=SanPham)
def taoQLSP(sender, instance, created, **kwargs):
    if created:
        QLSP.objects.create(
            maSP=instance, soLuongNhap=0, soLuongXuat=0, soLuongTonKho=0
        )


@receiver(post_save, sender=CTPN)
def themNhapHang(sender, instance, created, **kwargs):
    qlsp, created = QLSP.objects.get_or_create(maSP=instance.maSP)
    qlsp.soLuongNhap += instance.soLuongNhap
    qlsp.soLuongTonKho += instance.soLuongNhap
    qlsp.save()


@receiver(post_delete, sender=CTPN)
def xoaNhapHang(sender, instance, **kwargs):
    qlsp = QLSP.objects.get(maSP=instance.maSP)
    qlsp.soLuongNhap -= instance.soLuongNhap
    qlsp.soLuongTonKho -= instance.soLuongNhap
    qlsp.save()


@receiver(post_save, sender=CTHD)
def themXuatHang(sender, instance, created, **kwargs):
    qlsp, created = QLSP.objects.get_or_create(maSP=instance.maSP)
    qlsp.soLuongXuat += instance.soLuong
    qlsp.soLuongTonKho -= instance.soLuong
    qlsp.save()


@receiver(post_delete, sender=CTHD)
def xoaXuatHang(sender, instance, **kwargs):
    qlsp = QLSP.objects.get(maSP=instance.maSP)
    qlsp.soLuongXuat -= instance.soLuong
    qlsp.soLuongTonKho += instance.soLuong
    qlsp.save()
