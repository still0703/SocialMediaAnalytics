from backend.app import db
from datetime import datetime


class Keyword(db.Model):
    __tablename__ = 'keyword'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(100), nullable=False)  # 关键词内容
    importance = db.Column(db.Integer)  # 重要性级别
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 关联 users 表
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return f"<Keyword {self.word} (Importance: {self.importance})>"
