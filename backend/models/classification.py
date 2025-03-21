from backend.app import db
from datetime import datetime


class Classification(db.Model):
    __tablename__ = 'classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # 关联 posts 表
    category = db.Column(db.String(100), nullable=False)  # 类别名称
    confidence = db.Column(db.Float)  # 置信度
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)  # 分析时间，默认当前时间

    def __repr__(self):
        return f"<Classification {self.id}: {self.category} for Post {self.post_id}>"
