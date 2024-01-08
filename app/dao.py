from sqlalchemy.orm import Load

from app.models import UserRole, Khoi, LopHoc, HocSinh,Monhoc, Bangdiem, db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased

def load_function(user_role):
    if user_role == UserRole.nhanvien :
        return [
            {
                'name': 'Tiếp nhận học sinh',
                'url': '/tiepnhanhocsinh'
            },
            {
                'name': 'Lập danh sách',
                'url': '/danh-sach-lop'
            },
            {
                'name': 'Điều chỉnh danh sách',
                'url': '/dieuchinhdanhsach'
            },
        ]
    elif user_role == UserRole.giaovien:
        return [
            {
                'name': 'Điểm',
                'url': '/diem'
            },
            {
                'name': 'Kết quả học tập',
                'url': '/ketqua'
            }
        ]
    elif user_role == UserRole.quantri:
        return [
            {
                'name': 'Quy định môn học',
                'url': '/admin/khoi/'
            },
            {
                'name': 'Thống kê',
                'url': '/thongke'
            }
        ]
    return []

# read json and write json

def get_danh_sach_lop():
    khoi_list = Khoi.query.all()
    danh_sach_lop = {}
    for khoi in khoi_list:
        lop_list = LopHoc.query.filter_by(id_khoi=khoi.id).all()
        danh_sach_lop[khoi.ten] = lop_list
    return danh_sach_lop
def calculate_age(birthdate):
    today = datetime.now()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')  # Chuyển đổi ngày sinh từ string sang đối tượng datetime
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
def load_hocsinh(kw = None ):
    hocsinh = HocSinh.query
    if kw:
        hocsinh = hocsinh.filter(HocSinh.ten.contains(kw))

    return hocsinh.all()
def load_lop_trong():
    lop = LopHoc.query.all()
    loptrong =[]
    for lop in lop:
        if len(lop.hocsinhs) < lop.soluong:
            loptrong.append(lop)
    return loptrong
def is_Doi_Lop(ID_lophoc):
    loptrong = load_lop_trong()
    for lop in loptrong:
        if lop.ID_lophoc == ID_lophoc:
            return True
    return False
def Kiem_tra_mon_co_thuoc_lop_hay_khong(id_lop, id_monhoc):
    lop = LopHoc.query.get(id_lop)
    monhoc = Monhoc.query.get(id_monhoc)

    return monhoc in lop.khoi.monhocs if lop and monhoc else False
# số lượng đạt của lớp theo môn
def count_bangdiem(id_lophoc=None, id_monhoc=None, id_hocky=None):
    # Sử dụng and_ để kết hợp các điều kiện trong filter
    bangdiems = Bangdiem.query.filter(
        (Bangdiem.id_monhoc == id_monhoc) & (Bangdiem.id_lophoc == id_lophoc) & (Bangdiem.id_hocky == id_hocky)
    )
    count = 0
    for bangdiem in bangdiems:
        if bangdiem.diem_trung_binh_mon >= 5:
            count += 1
    return count

# sỉ số học sinh của lớp
def siso(id_lophoc):
    lophoc = LopHoc.query.filter(LopHoc.ID_lophoc == id_lophoc).first()
    return len(lophoc.hocsinhs) if lophoc else 0

# tỷ lệ đạt của 1 lớp trong 1 môn ở 1 học kỳ
def tyledat(id_lophoc=None, id_monhoc=None, id_hocky=None):
    sisos = siso(id_lophoc)
    baidat = count_bangdiem(id_lophoc, id_monhoc, id_hocky)
    return baidat * 100 / sisos if sisos > 0 else 0




