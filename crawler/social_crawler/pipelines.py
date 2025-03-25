import pymysql
from itemadapter import ItemAdapter
from .items import PostItem, CommentItem


class DatabasePipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='social_media_analytics',
            charset='utf8mb4'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, PostItem):
            # 检查是否已存在相同URL的帖子
            self.cursor.execute(
                "SELECT id FROM posts WHERE url = %s",
                (adapter.get('url'),)
            )
            existing_post = self.cursor.fetchone()

            if not existing_post:
                sql = """
                INSERT INTO posts 
                (original_id, author, content, post_time, crawled_time, url, likes, comments, shares)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(
                    sql,
                    (
                        adapter.get('original_id'),
                        adapter.get('author'),
                        adapter.get('content'),
                        adapter.get('post_time'),
                        adapter.get('crawled_time'),
                        adapter.get('url'),
                        adapter.get('likes'),
                        adapter.get('comments'),
                        adapter.get('shares')
                    )
                )
                self.connection.commit()
                return item
            else:
                spider.logger.info(f"Duplicate post URL found: {adapter.get('url')}")
                return None

        elif isinstance(item, CommentItem):
            # 首先需要找到对应post在数据库中的ID
            self.cursor.execute(
                "SELECT id FROM posts WHERE original_id = %s",
                (adapter.get('post_id'),)
            )
            post_result = self.cursor.fetchone()

            if post_result:
                post_id = post_result[0]
                # 检查是否已存在相同内容和作者的评论
                self.cursor.execute(
                    "SELECT id FROM comments WHERE post_id = %s AND author = %s AND content = %s",
                    (post_id, adapter.get('author'), adapter.get('content'))
                )
                existing_comment = self.cursor.fetchone()

                if not existing_comment:
                    sql = """
                    INSERT INTO comments 
                    (post_id, author, content, comment_time, crawled_time, likes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(
                        sql,
                        (
                            post_id,
                            adapter.get('author'),
                            adapter.get('content'),
                            adapter.get('comment_time'),
                            adapter.get('crawled_time'),
                            adapter.get('likes')
                        )
                    )
                    self.connection.commit()
                    return item
                else:
                    spider.logger.info(f"Duplicate comment found for post {post_id}")
                    return None

        return item