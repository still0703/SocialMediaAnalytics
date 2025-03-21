from backend.app import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_id = db.Column(db.String(100))  # 原平台上的帖子ID
    author = db.Column(db.String(100))  # 发帖作者
    content = db.Column(db.Text, nullable=False)  # 帖子内容
    post_time = db.Column(db.DateTime)  # 发帖时间
    crawled_time = db.Column(db.DateTime, default=datetime.utcnow)  # 爬取时间，默认为当前时间
    url = db.Column(db.String(255))  # 帖子URL
    likes = db.Column(db.Integer, default=0)  # 点赞数
    comments = db.Column(db.Integer, default=0)  # 评论数
    shares = db.Column(db.Integer, default=0)  # 分享数

    def __repr__(self):
        return f"<Post {self.id}: {self.original_id}>"
