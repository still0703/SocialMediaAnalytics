from backend.app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(255), nullable=False)
    posted_time = db.Column(db.DateTime, nullable=False)
    crawled_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 情感分析结果
    sentiment = db.Column(db.String(20), nullable=True)  # positive, neutral, negative
    confidence = db.Column(db.Float, nullable=True)

    # 分类结果
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Post {self.id}>'