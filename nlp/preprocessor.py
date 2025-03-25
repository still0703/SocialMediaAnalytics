import re
import jieba
import jieba.posseg as pseg
import html
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Config
from backend.models.post import Post
from backend.models.comments import Comment


class DatabasePreprocessor:
    def __init__(self, stopwords_path: str = None):
        """
        初始化数据库预处理器

        :param stopwords_path: 停用词文件路径，默认为None
        """
        # 加载停用词
        self.stopwords = self._load_stopwords(stopwords_path)

        # 初始化数据库引擎
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def _load_stopwords(self, path: str = None) -> set:
        """
        加载停用词

        :param path: 停用词文件路径
        :return: 停用词集合
        """
        default_stopwords = {
            '的', '了', '和', '是', '就', '都', '与', '或',
            '为', '在', '啊', '哦', '呢', '吧', '吗', '呀'
        }

        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_stopwords = set(line.strip() for line in f)
                return default_stopwords.union(file_stopwords)
            except FileNotFoundError:
                print(f"Warning: Stopwords file {path} not found. Using default stopwords.")

        return default_stopwords

    def clean_text(self, text: str) -> str:
        """
        文本清洗

        :param text: 原始文本
        :return: 清洗后的文本
        """
        if not isinstance(text, str):
            return ''

        # 解码HTML实体
        text = html.unescape(text)

        # 去除URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # 去除特殊符号和标点
        text = re.sub(r'[^\u4e00-\u9fff\w\s]', '', text)

        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize(self, text: str, with_stopwords: bool = False) -> list:
        """
        中文分词

        :param text: 待分词文本
        :param with_stopwords: 是否保留停用词
        :return: 分词结果列表
        """
        words = jieba.lcut(text)

        if not with_stopwords:
            words = [word for word in words if word not in self.stopwords]

        return words

    def preprocess_posts(self, batch_size: int = 1000):
        """
        批量预处理帖子数据

        :param batch_size: 每次处理的数据量
        """
        session = self.Session()

        try:
            # 查询未处理的帖子
            query = text("""
                SELECT id, content 
                FROM posts 
                WHERE preprocessed = 0 OR preprocessed IS NULL 
                LIMIT :batch_size
            """)

            results = session.execute(query, {'batch_size': batch_size})

            for row in results:
                post_id = row.id
                original_content = row.content

                # 文本清洗
                cleaned_content = self.clean_text(original_content)

                # 分词
                tokens = self.tokenize(cleaned_content)
                tokens_str = ','.join(tokens)

                # 更新数据库
                update_query = text("""
                    UPDATE posts 
                    SET cleaned_content = :cleaned_content, 
                        tokens = :tokens, 
                        preprocessed = 1 
                    WHERE id = :post_id
                """)

                session.execute(update_query, {
                    'cleaned_content': cleaned_content,
                    'tokens': tokens_str,
                    'post_id': post_id
                })

            # 提交事务
            session.commit()

            print(f"成功预处理 {results.rowcount} 条帖子数据")

        except Exception as e:
            session.rollback()
            print(f"预处理帖子数据时发生错误: {e}")

        finally:
            session.close()

    def preprocess_comments(self, batch_size: int = 1000):
        """
        批量预处理评论数据

        :param batch_size: 每次处理的数据量
        """
        session = self.Session()

        try:
            # 查询未处理的评论
            query = text("""
                SELECT id, content 
                FROM comments 
                WHERE preprocessed = 0 OR preprocessed IS NULL 
                LIMIT :batch_size
            """)

            results = session.execute(query, {'batch_size': batch_size})

            for row in results:
                comment_id = row.id
                original_content = row.content

                # 文本清洗
                cleaned_content = self.clean_text(original_content)

                # 分词
                tokens = self.tokenize(cleaned_content)
                tokens_str = ','.join(tokens)

                # 更新数据库
                update_query = text("""
                    UPDATE comments 
                    SET cleaned_content = :cleaned_content, 
                        tokens = :tokens, 
                        preprocessed = 1 
                    WHERE id = :comment_id
                """)

                session.execute(update_query, {
                    'cleaned_content': cleaned_content,
                    'tokens': tokens_str,
                    'comment_id': comment_id
                })

            # 提交事务
            session.commit()

            print(f"成功预处理 {results.rowcount} 条评论数据")

        except Exception as e:
            session.rollback()
            print(f"预处理评论数据时发生错误: {e}")

        finally:
            session.close()


def main():
    # 创建预处理器实例
    preprocessor = DatabasePreprocessor()

    # 预处理帖子数据
    preprocessor.preprocess_posts()

    # 预处理评论数据
    preprocessor.preprocess_comments()


if __name__ == "__main__":
    main()