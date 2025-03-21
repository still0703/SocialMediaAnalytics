from backend.app import db


class KeywordPost(db.Model):
    __tablename__ = 'keyword_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), nullable=False)  # 关联 keywords 表
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # 关联 posts 表
    match_count = db.Column(db.Integer, default=0)  # 匹配次数

    def __repr__(self):
        return f"<KeywordPost id:{self.id} keyword_id:{self.keyword_id} post_id:{self.post_id} match_count:{self.match_count}>"
