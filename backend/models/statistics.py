from backend.app import db
from datetime import date


class Statistics(db.Model):
    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)  # 统计日期
    total_posts = db.Column(db.Integer, default=0)  # 帖子总数
    positive_count = db.Column(db.Integer, default=0)  # 正面帖子数
    neutral_count = db.Column(db.Integer, default=0)  # 中性帖子数
    negative_count = db.Column(db.Integer, default=0)  # 负面帖子数
    hot_topics = db.Column(db.Text)  # 热门话题，存储JSON字符串
    keywords_frequency = db.Column(db.Text)  # 关键词频率，存储JSON字符串

    def __repr__(self):
        return f"<DailyStatistics {self.date}>"
