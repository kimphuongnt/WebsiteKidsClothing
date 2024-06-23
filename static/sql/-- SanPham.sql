-- SanPham
INSERT INTO
    home_sanpham (
        maSP,
        tenSP,
        moTa,
        giaBan,
        chatLieu,
        mauSac,
        gioiTinh,
        hinhanh,
        hinhanh1,
        hinhanh2,
        maDM_id,
        maNCC_id,
        maNH_id
    )
VALUES
    (
        'SP001',
        'Áo hoodie',
        'Áo hoodie nam chất liệu cotton',
        150000,
        'Cotton',
        'Đen',
        'NAM',
        'images/sanpham/hoodieden.jpg',
        'images/sanpham/hoodie2.jpg',
        'images/sanpham/hoodie3.jpg',
        'AT',
        'VT',
        'ZR'
    ),
    (
        'SP002',
        'Áo thun nữ',
        'Áo thun nữ thiết kế đơn giản',
        100000,
        'Cotton',
        'Trắng',
        'NU',
        'images/sanpham/aothun1.jpg',
        'images/sanpham/aothun2.jpg',
        'images/sanpham/aothun3.jpg',
        'AT',
        'TD',
        'HM'
    ),
    (
        'SP003',
        'Quần short nam',
        'Quần short nam thoáng mát',
        120000,
        'Kaki',
        'Xanh',
        'NAM',
        'images/sanpham/short1.jpg',
        'images/sanpham/short2.jpg',
        'images/sanpham/short3.jpg',
        'QS',
        'KC',
        'CNF'
    ),
    (
        'SP004',
        'Đầm ngắn tay công chúa',
        'Đầm ngắn tay phong cách công chúa',
        250000,
        'Voan',
        'Hồng',
        'NU',
        'images/sanpham/dam1.jpg',
        'images/sanpham/dam2.jpg',
        'images/sanpham/dam3.jpg',
        'DCC',
        'MZ',
        'MS'
    ),
    (
        'SP005',
        'Áo khoác nam',
        'Áo khoác nam chống nắng',
        200000,
        'Polyester',
        'Đỏ',
        'NAM',
        'images/sanpham/khoac1.jpg',
        'images/sanpham/khoac2.jpg',
        'images/sanpham/khoac3.jpg',
        'AK',
        'VX',
        'HBK'
    ),
    (
        'SP006',
        'Áo dài tay nữ',
        'Áo dài tay nữ mùa đông',
        180000,
        'Len',
        'Xám',
        'NU',
        'images/sanpham/daitay1.jpg',
        'images/sanpham/daitay2.jpg',
        'images/sanpham/daitay3.jpg',
        'ADT',
        'VT',
        'GK'
    )

INSERT INTO
    home_qlsp (soLuongNhap, soLuongXuat, soLuongTonKho, maSP_id)
VALUES
    (100, 50, 50, 'SP001'),
    (80, 40, 40, 'SP002'),
    (80, 40, 40, 'SP003'),
    (80, 40, 40, 'SP004'),
    (80, 40, 40, 'SP005'),
    (80, 40, 40, 'SP006')
