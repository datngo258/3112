import hashlib

from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, login
from app.models import *
import dao


@login.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template('index.html', funcs=funcs)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == str(hashlib.md5(request.form.get("pswd").encode('utf-8')).hexdigest()):
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/tiepnhanhocsinh')
def tiepNhanHocSinh():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("tiepNhanHocSinh.html", funcs=funcs)


@app.route('/lapdanhsach')
def lapDanhSach():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("lapDanhSach.html", funcs=funcs)
@app.route('/dieuchinhdanhsach', methods=['GET', 'POST'])
def dieuChinhDanhSach():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    kw = request.args.get('keyword')
    hocsinhs = dao.load_hocsinh(kw=kw)
    lops = dao.load_lop_trong()
    if request.method == 'POST':
        id_hs = request.form['id_hs']
        id_LopHoc =request.form['id_LopHoc']

        hs = HocSinh.query.filter_by(id=id_hs).first()
        lop = LopHoc.query.filter_by(ID_lophoc=id_LopHoc).first()

        if hs is None or lop is None:
            thongbao = '? Kiểm tra lại thông tin đã nhập.'
            return render_template('dieuchinhdanhsach.html', funcs=funcs,hocsinhs= hocsinhs,lops=lops, tb=thongbao )
        else :
            if hs.lophoc.id_khoi == lop.id_khoi:
                if lop and len(lop.hocsinhs) < lop.soluong:
                    hs.lophoc_id = id_LopHoc
                    db.session.commit()
                    thongbao = 'Hoàn thànhhhhhhhhhhh  !!!!!!'
                    return render_template('dieuchinhdanhsach.html', funcs=funcs, hocsinhs=hocsinhs, lops=lops,
                                           tb=thongbao)
                else:
                    thongbao = 'Lớp đã đầyyyyyyyyyy .'
                    return render_template('dieuchinhdanhsach.html', funcs=funcs, hocsinhs=hocsinhs, lops=lops,
                                           tb=thongbao)
            else :
                thongbao = 'Lớp không thuộc khối của học sinh muốn đổi !!!!!!'
                return render_template('dieuchinhdanhsach.html', funcs=funcs, hocsinhs=hocsinhs, lops=lops,
                                       tb=thongbao)

    return render_template("dieuChinhDanhSach.html", funcs=funcs,hocsinhs= hocsinhs,lops=lops)
@app.route('/quydinh')
def quyDinh():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("quyDinh.html", funcs=funcs)


@app.route('/thongke')
def thongKe():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("thongKe.html", funcs=funcs)


@app.route('/diem')
def diem():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("diem.html", funcs=funcs)
@app.route('/danh-sach-lop')
def danh_sach_lop():
    danh_sach_lop_data = dao.get_danh_sach_lop()
    return render_template('danh_sach_lop.html', danh_sach_lop=danh_sach_lop_data)
@app.route('/them-hoc-sinh', methods=['GET', 'POST'])
def them_hoc_sinh():
    if request.method == 'POST':
        ten = request.form['name']
        gioitinh = request.form['gioitinh']
        ngaysinh = request.form['ngaysinh']
        diachi = request.form['Diachi']
        email = request.form['email']
        #khoi_id = 1
        # tính khoi_id nếu age <= 16 --1
        # nếu  16 < age < 17 ---2
        # nếu  17 < age --- 3
        age = dao.calculate_age(ngaysinh)
        if  age < app.config['mintuoi'] or age > app.config['maxtuoi'] :
            return render_template('tiepnhanhocsinh.html', msg='Tuổi không hợp lệ. Vui lòng kiểm tra lại.')
        if age <= 16 :
            khoi_id = 1
        elif 16 < age <= 17 :
            khoi_id = 2
        elif age > 17 :
            khoi_id =3


        # Lấy danh sách lớp của khối
        lop_list = LopHoc.query.filter_by(id_khoi=khoi_id).all()

        # Kiểm tra lớp có thể thêm học sinh hay không
        for lopp in lop_list:
            if len(lopp.hocsinhs) < lopp.soluong:
                hoc_sinh = HocSinh(ten=ten, gioitinh=gioitinh, ngaysinh=ngaysinh, diachi=diachi, email=email, lophoc_id=lopp.ID_lophoc)
                db.session.add(hoc_sinh)
                db.session.commit()

                return redirect(url_for('danh_sach_lop'))

        # Nếu không có lớp nào chưa đầy, tạo lớp mới và thêm học sinh vào đó
        new_lop = LopHoc(TenLop=f'Lớp {len(lop_list) + 1}', id_khoi=khoi_id)
        db.session.add(new_lop)
        db.session.commit()

        hoc_sinh = HocSinh(ten=ten, gioitinh=gioitinh, ngaysinh=ngaysinh, diachi=diachi, email=email, lophoc_id=new_lop.ID_lophoc)
        db.session.add(hoc_sinh)
        db.session.commit()

        return redirect(url_for('danh_sach_lop'))

    khoi_list = Khoi.query.all()
    return render_template('tiepnhanhocsinh.html', khoi_list=khoi_list)



if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
