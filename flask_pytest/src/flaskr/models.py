"""
宣告資料表欄位
"""
from .main import db


class User(db.Model):
    # 設定 primary_key
    guid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
