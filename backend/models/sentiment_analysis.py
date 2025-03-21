from backend.app import db
from datetime import datetime


class SentimentAnalysis(db.Model):
    __tablename__ = 'sentiment_analysis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content_type = db.Column(db.String(20), nullable=False)  # 'post' 或 'comment'
    content_id = db.Column(db.Integer, nullable=False)  # 对应 posts 或 comments 的 ID
    sentiment = db.Column(db.String(20), nullable=False)  # 情感倾向: positive/neutral/negative
    confidence = db.Column(db.Float)  # 置信度
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)  # 分析时间，默认当前时间

    def __repr__(self):
        return f"<SentimentAnalysis {self.id} - {self.content_type}:{self.content_id}>"
