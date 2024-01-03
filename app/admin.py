from flask_admin import Admin
from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import HocSinh,UserRole, User, LopHoc, Khoi
from datetime import datetime
admin = Admin(app=app, name='Tiếp nhận Học Sinh', template_mode='bootstrap4')

class StudentAdmin(ModelView):
    def on_model_change(self, form, model, is_created):
        # Kiểm tra điều kiện về độ tuổi (15 - 20)
        if model.ngaysinh:
            today = datetime.now().date()
            age = today.year - model.ngaysinh.year - (
                    (today.month, today.day) < (model.ngaysinh.month, model.ngaysinh.day))
            if not (15 <= age <= 20):
                raise ValueError("Độ tuổi của học sinh phải từ 15 đến 20.")
class MyStudent(StudentAdmin):
    can_view_details = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['ten']
    column_filters = ['ten']
    can_export = True
    column_list = ('id', 'ten', 'ngaysinh', 'gioitinh', 'lophoc_id')
    form_columns = ('ten', 'ngaysinh', 'gioitinh', 'email', 'diachi', 'lophoc_id')
class LopHocView(ModelView):
    column_list = ('ID_lophoc','TenLop','id_khoi','hocsinhs','soluong')
    form_columns = ('TenLop','id_khoi','soluong')
admin.add_view(MyStudent(HocSinh, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(LopHocView(LopHoc, db.session))
admin.add_view(ModelView(Khoi, db.session))

