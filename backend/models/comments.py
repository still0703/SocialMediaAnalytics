from backend.app import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # 关联posts表
    author = db.Column(db.String(100))  # 评论作者
    content = db.Column(db.Text, nullable=False)  # 评论内容
    comment_time = db.Column(db.DateTime)  # 评论时间
    crawled_time = db.Column(db.DateTime, default=datetime.utcnow)  # 爬取时间，默认当前时间
    likes = db.Column(db.Integer, default=0)  # 点赞数

    def __repr__(self):
        return f"<Comment {self.id} on Post {self.post_id}>"
