import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kullaniciadi:parola@localhost:3306/veritabaniadi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
