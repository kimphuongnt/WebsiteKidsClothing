-- SQLite
-- SQLite
--Category
INSERT INTO
    home_category (maCate, tenCate)
VALUES
    ('AO', 'Áo'),
    ('QUAN', 'Quần'),
    ('DAM', 'Đầm'),
    ('DOBO', 'Đồ bộ'),
    ('PK', 'Phụ kiện'),
    ('KH', 'Khác');

-- Danh mục
INSERT INTO
    home_danhmuc (maDM, tenDM, maCate_id)
VALUES
    ('DNT', 'Đầm ngắn tay', 'DAM'),
    ('DDT', 'Đầm ngắn tay', 'DAM'),
    ('DHD', 'Đầm hai dây', 'DAM'),
    ('DCC', 'Đầm công chúa', 'DAM'),
    ('CV', 'Chân váy', 'DAM');

INSERT INTO
    home_danhmuc (maDM, tenDM, maCate_id)
VALUES
    ('AT', 'Áo thun', 'AO'),
    ('AK', 'Áo khoác', 'AO'),
    ('ADT', 'Áo dài tay', 'AO');

INSERT INTO
    home_danhmuc (maDM, tenDM, maCate_id)
VALUES
    ('QS', 'Quần short', 'QUAN'),
    ('QD', 'Quần dài', 'QUAN');

INSERT INTO
    home_danhmuc (maDM, tenDM, maCate_id)
VALUES
    ('DBNT', 'Đồ bộ ngắn tay', 'DOBO'),
    ('DBDT', 'Đồ bộ dài tay', 'DOBO');

INSERT INTO
    home_danhmuc (maDM, tenDM, maCate_id)
VALUES
    ('PK', 'Phụ kiện', 'PHUKIEN');

--NhanHieu
INSERT INTO
    home_nhanhieu (maNH, tenNH, xuatXu)
VALUES
    ('ZR', 'Zara Kids', 'Tây Ban Nha'),
    ('CNF', 'Canifa Kid', 'Việt Nam'),
    ('HM', 'H&M Kids', 'Thụy Điển'),
    ('RB', 'Rabity', 'Việt Nam'),
    ('MS', 'MunsterKids', 'Úc'),
    ('HBK', 'Hugo Boss Kids', 'Đức'),
    ('GK', 'Gap Kids', 'Mỹ');

--NhaCungCap
INSERT INTO
    home_nhacungcap (maNCC, tenNCC, diaChi, soDT, eMail)
VALUES
    (
        'VT',
        'Công Ty Cổ Phần May Vĩnh Tiến',
        'CCN Hà Mãn, Trí Quả, X. Hà Mãn, H. Thuận Thành, Bắc Ninh',
        '0968682726',
        'vungtienkids@gmail.com'
    ),
    (
        'TD',
        'Công Ty TNHH Sản Xuất Thương Mại Dịch Vụ Tiến Tiến Đạt',
        'Số 48 Nguyễn Thanh Đằng, Phường Phước Trung, Thành Phố Bà Rịa, Bà Rịa-Vũng Tàu, Việt Nam',
        '0906010809',
        'tiendat@gmail.com'
    ),
    (
        'KC',
        'Công Ty TNHH Thời Trang Kico',
        'Lô 15, Khu A1, KĐT Đại Kim Định Công, P. Định Công, Q. Hoàng Mai, Hà Nội, Việt Nam',
        '0938726137',
        'kico@gmail.com'
    ),
    (
        'MZ',
        'MZ Kids Wear & Swimwear Manufacturer',
        'Tầng 4, Guangcai Innovation Park, Số 29, Đường Yibin, Quận Huli, Hạ Môn, Trung Quốc',
        '5922652304',
        'MZ@gmail.com'
    ),
    (
        'VX',
        'Công Ty TNHH Xuất Nhập Khẩu Vườn Xuân',
        '282 Nguyễn Lương Bằng, P. Tân Phú, Q.7 Tp. Hồ Chí Minh, Việt Nam',
        '0935923690',
        'vuonxuan@gmail.com'
    );

--KichCo
INSERT INTO
    home_kichco (maSize, tenSize)
VALUES
    ('S', 'Nhỏ'),
    ('M', 'Vừa'),
    ('L', 'Lớn');

--SanPham
