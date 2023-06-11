from sqlalchemy import Column, String, Integer, Date, Boolean, Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    name = Column(String)
    email = Column(String)
    telp = Column(String)
    password = Column(String)
    nik = Column(String)
    alamat = Column(String)
    ttl = Column(Date)
    gol_darah = Column(String)
    rhesus = Column(String)
    gender = Column(String)
    last_donor = Column(Date)
    photo = Column(String)
    refresh_token = Column(Text)
    verified = Column(Boolean, default=False)

    def __init__(self, id, uid, name, email, telp, password, nik, alamat, ttl, gol_darah, rhesus, gender, last_donor, photo, refresh_token, verified):
        self.id = id
        self.uid = uid
        self.name = name
        self.email = email
        self.telp = telp
        self.password = password
        self.nik = nik
        self.alamat = alamat
        self.ttl = ttl
        self.gol_darah = gol_darah
        self.rhesus = rhesus
        self.gender = gender
        self.last_donor = last_donor
        self.photo = photo
        self.refresh_token = refresh_token
        self.verified = verified