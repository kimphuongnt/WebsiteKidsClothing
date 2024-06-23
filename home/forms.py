from django import forms
from .models import HoaDon, KhachHang, Review


class KhachHangLoginForm(forms.Form):
    tenDN = forms.CharField(max_length=50, label="Tên đăng nhập")
    matKhau = forms.CharField(
        max_length=50, widget=forms.PasswordInput, label="Mật khẩu"
    )


class KhachHangRegistrationForm(forms.ModelForm):
    matKhau = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    matKhau_xacNhan = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu")

    class Meta:
        model = KhachHang
        fields = ['tenKH', 'soDT', 'eMail', 'diaChi', 'tenDN', 'matKhau']

    def clean_tenDN(self):
        tenDN = self.cleaned_data.get('tenDN')
        if len(tenDN) < 5 or len(tenDN) > 10:
            raise forms.ValidationError("Tên đăng nhập phải từ 5 đến 10 ký tự")
        if KhachHang.objects.filter(tenDN=tenDN).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại")
        return tenDN

    def clean_soDT(self):
        soDT = self.cleaned_data.get('soDT')
        if KhachHang.objects.filter(soDT=soDT).exists():
            raise forms.ValidationError("Số điện thoại đã được sử dụng")
        if len(soDT) !=10: 
            raise forms.ValidationError("Số điện thoại nhập không hợp lệ")
        return soDT

    def clean_eMail(self):
        eMail = self.cleaned_data.get('eMail')
        if not forms.EmailField().clean(eMail):
            raise forms.ValidationError("Địa chỉ email không hợp lệ")
        return eMail

    def clean_matKhau_xacNhan(self):
        matKhau = self.cleaned_data.get('matKhau')
        matKhau_xacNhan = self.cleaned_data.get('matKhau_xacNhan')
        if matKhau and matKhau_xacNhan and matKhau != matKhau_xacNhan:
            raise forms.ValidationError("Mật khẩu xác nhận không khớp")
        return matKhau_xacNhan

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = HoaDon
        fields = ["diaChi", "soDienThoai", "ghiChu"]

    diaChi = forms.CharField(max_length=255, label="Địa chỉ")
    soDienThoai = forms.CharField(max_length=20, label="Số điện thoại")
    ghiChu = forms.CharField(widget=forms.Textarea, required=False, label="Ghi chú")


class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ["tenKH", "soDT", "diaChi", "eMail", "gioiTinh"]

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu cũ")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu mới")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu mới")

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Mật khẩu xác nhận không khớp.")
        return cleaned_data
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['diemDanhGia', 'danhGia']
        widgets = {
            'diemDanhGia': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'danhGia': forms.Textarea(attrs={'rows': 5}),
        }