from flask_login import UserMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Boolean,BOOLEAN,Date
from sqlalchemy.orm import relationship
from app import app, db
import enum
from datetime import datetime
from enum import Enum as UserEnum


class UserRole(UserEnum):
    giaovien = 1
    quantri = 2
    nhanvien = 3
User_LopHoc = db.Table('User_LopHoc',
                       Column('id_user', Integer, ForeignKey('user.id'), nullable=True),
                       Column('id_LopHoc', Integer, ForeignKey('LopHoc.ID_lophoc'), nullable=True)
                       )
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.giaovien)
    active = Column(BOOLEAN, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    lops = relationship('LopHoc', secondary=User_LopHoc, backref='user', lazy=True   )

class HocSinh(db.Model):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=False)
    gioitinh = Column(Enum('Male', 'Female',))
    ngaysinh = Column(Date)
    diachi = Column(String(100))
    email = Column(String(100))
    lophoc_id = Column(Integer, ForeignKey('LopHoc.ID_lophoc'), nullable=False)
    ds_bangdiem = relationship('Bangdiem', backref='hocsinh', lazy=True)
    def __str__(self):
        return self.ten
class LopHoc(db.Model):
    __tablename__ = 'LopHoc'
    ID_lophoc = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    TenLop = Column(String(50), nullable=False)
    hocsinhs = relationship('HocSinh', backref='lophoc', lazy=True)
    soluong = Column(Integer, default=app.config['soluong'], nullable=False)
    id_khoi = Column(Integer, ForeignKey('khoi.id'), nullable=False)

    def __str__(self):
        return str(self.id_khoi) + "/" + self.TenLop + "----" + str(self.ID_lophoc)
khoi_monhoc = db.Table('khoi_monhoc',
                       Column('id_khoi', Integer, ForeignKey('khoi.id'), nullable=True),
                       Column('id_mon', Integer, ForeignKey('monhoc.id'), nullable=True)
                       )

class Khoi(db.Model):
    __tablename__ = 'khoi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    lops = relationship('LopHoc', backref='khoi', lazy=True)
    monhocs = relationship('Monhoc', secondary= khoi_monhoc , backref='khoi', lazy=True)

    def __str__(self):
        return self.ten
class Monhoc(db.Model):
    __tablename__ = 'monhoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    bangdiems = relationship('Bangdiem', backref='subject', lazy=True)
    def __str__(self):
        return self.name


class Hocky(db.Model):
    __tablename__ = 'hocky'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    # HK1_23
    namhoc = Column(Integer)
    bangdiems = relationship('Bangdiem', backref='hocky', lazy=True)
    def __str__(self):
        return self.name +'/' + self.namhoc


class Bangdiem(db.Model):
    __tablename__ = 'bangdiem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_lophoc = Column(Integer, ForeignKey(LopHoc.ID_lophoc), nullable=False)
    id_monhoc = Column(Integer, ForeignKey(Monhoc.id), nullable=False)
    id_hocky = Column(Integer, ForeignKey(Hocky.id), nullable=False)
    id_hocsinh = Column(Integer, ForeignKey(HocSinh.id), nullable=False)
    diem_15phut = Column(Float)
    diem_1tiet = Column(Float)
    diem_ck = Column(Float)
    diem_trung_binh_mon = Column(Float)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

