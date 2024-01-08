import hashlib
import numpy as np
from Tools.scripts.var_access_benchmark import B
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_login import login_user, logout_user, current_user
from app import app, login
from app.models import *
import dao
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import literal
from sqlalchemy import func,case, and_
from wtforms.validators import DataRequired


min , max



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

    return render_template('quydinh.html', funcs=funcs)
@app.route('/thongke')
def thongKe():
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    ds_lop = LopHoc.query.all()
    data = []
    stt =1
    for hocky in range(1,3):
        id_hocky = hocky
        for lop in ds_lop:
            id_lop = lop.ID_lophoc
            id_khoi = lop.id_khoi

            for monhoc in lop.khoi.monhocs:
                id_monhoc = monhoc.id

                sisos = dao.siso(id_lop)
                baidat = dao.count_bangdiem(id_lop, id_monhoc,id_hocky)
                ty_le_dat_mon = baidat*100  / (sisos) if sisos > 0 else 0

                data.append({
                    'stt': stt,
                    'ten_lop': lop.TenLop,
                    'hoc_ky':  id_hocky,
                    'ten_mon': monhoc.name,  # Đặt tên môn học tùy thuộc vào cách bạn lưu trữ trong model
                    'si_so': sisos,
                    'id_khoi':id_khoi,
                    'so_bai_dat': baidat,
                    'ty_le_dat': ty_le_dat_mon
                })
                stt +=1

    return render_template("thongke.html", data=data, funcs=funcs)

@app.route('/diem', methods=['GET', 'POST'])
def diem():
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    if request.method == 'POST':
        try:
            for lop in current_user.lops:
                for monhoc in lop.khoi.monhocs:
                    for hocsinh in lop.hocsinhs:
                        id_hocsinh = hocsinh.id
                        id_monhoc = monhoc.id

                        for hocky in range(1, 3):
                            diem15p_str = request.form.get(f'diem15p_{id_hocsinh}_{id_monhoc}_{hocky}')
                            diem45p_str = request.form.get(f'diem45p_{id_hocsinh}_{id_monhoc}_{hocky}')
                            diemck_str = request.form.get(f'diemck_{id_hocsinh}_{id_monhoc}_{hocky}')

                            if diem15p_str is not None and diem45p_str is not None and diemck_str is not None:
                                diem15p = list(map(float, diem15p_str.split(',')))
                                diem45p = list(map(float, diem45p_str.split(',')))
                                diemck = float(diemck_str)

                                diem_15phut = np.mean(diem15p) if diem15p else None
                                diem_1tiet = np.mean(diem45p) if diem45p else None
                                average_value = np.mean([diem_15phut, diem_1tiet, diemck])

                                # Kiểm tra và xóa bảng cũ nếu có
                                existing_bangdiem = Bangdiem.query.filter_by(
                                    id_lophoc=lop.ID_lophoc, id_monhoc=id_monhoc, id_hocky=hocky, id_hocsinh=id_hocsinh
                                ).first()

                                if existing_bangdiem:
                                    # Nếu bảng cũ tồn tại, cập nhật giá trị của nó
                                    existing_bangdiem.diem_15phut = diem_15phut
                                    existing_bangdiem.diem_1tiet = diem_1tiet
                                    existing_bangdiem.diem_ck = diemck
                                    existing_bangdiem.diem_trung_binh_mon = average_value

                                    try:
                                        db.session.merge(existing_bangdiem)
                                        db.session.commit()
                                    except Exception as e:
                                        db.session.rollback()
                                        return jsonify({'error': str(e)})
                                else:
                                    # Nếu bảng cũ không tồn tại, tạo bảng mới
                                    new_bangdiem = Bangdiem(
                                        id_lophoc=lop.ID_lophoc, id_monhoc=id_monhoc, id_hocky=hocky,
                                        id_hocsinh=id_hocsinh, diem_15phut=diem_15phut,
                                        diem_1tiet=diem_1tiet, diem_ck=diemck,
                                        diem_trung_binh_mon=average_value
                                    )

                                    # Thêm mới hoặc cập nhật thông tin
                                    try:
                                        db.session.add(new_bangdiem)
                                        db.session.commit()
                                    except Exception as e:
                                        db.session.rollback()
                                        return jsonify({'error': str(e)})

        except Exception as e:
            return jsonify({'error': str(e)})

    ds_lop = current_user.lops
    return render_template("diem.html", lops=ds_lop, funcs=funcs)

@app.route("/ketqua")
def ketqua():
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    ds_lop = current_user.lops  # Thay thế với danh sách lớp thực tế của bạn

    data = []  # Dữ liệu xuất điểm

    for lop in ds_lop:
        for monhoc in lop.khoi.monhocs:
            for hocsinh in lop.hocsinhs:
                hocky_1 = Bangdiem.query.filter_by(id_lophoc=lop.ID_lophoc, id_monhoc=monhoc.id, id_hocsinh=hocsinh.id,
                                                   id_hocky=1).first()
                hocky_2 = Bangdiem.query.filter_by(id_lophoc=lop.ID_lophoc, id_monhoc=monhoc.id, id_hocsinh=hocsinh.id,
                                                   id_hocky=2).first()
                # hocky_1 = Bangdiem.query.filter_by(
                #     id_lophoc=lop.ID_lophoc, id_monhoc=monhoc.id, id_hocsinh=hocsinh.id, id_hocky=1
                # ).order_by(Bangdiem.id.desc()).first()
                #
                # hocky_2 = Bangdiem.query.filter_by(
                #     id_lophoc=lop.ID_lophoc, id_monhoc=monhoc.id, id_hocsinh=hocsinh.id, id_hocky=2
                # ).order_by(Bangdiem.id.desc()).first()

                diem_tb_hk1 = hocky_1.diem_trung_binh_mon if hocky_1 else None
                diem_tb_hk2 = hocky_2.diem_trung_binh_mon if hocky_2 else None

                data.append({
                    'ten_hocsinh': hocsinh.ten,
                    'lop': lop.TenLop,
                    'mon_hoc': monhoc.name,
                    'diem_tb_hk1': diem_tb_hk1,
                    'diem_tb_hk2': diem_tb_hk2
                })


    return render_template("xeplop.html", data = data  , funcs=funcs)
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
