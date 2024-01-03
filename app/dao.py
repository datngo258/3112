from sqlalchemy.orm import Load

from app.models import UserRole, Khoi, LopHoc, HocSinh
from datetime import datetime
from sqlalchemy import func

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
            }
        ]
    elif user_role == UserRole.quantri:
        return [
            {
                'name': 'Quy định',
                'url': '/quydinh'
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