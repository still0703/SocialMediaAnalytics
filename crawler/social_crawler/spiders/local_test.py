import scrapy
from datetime import datetime
from ..items import PostItem, CommentItem


class LocalTestSpider(scrapy.Spider):
    name = "local_test"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:8000/test.html"]

    def parse(self, response):
        # 提取所有帖子
        posts = response.css('div.post')

        for post in posts:
            post_item = PostItem()
            post_item['original_id'] = post.css('::attr(data-post-id)').get()
            post_item['author'] = post.css('.author::text').get()
            post_item['content'] = post.css('.content::text').get()
            post_item['post_time'] = post.css('.time::text').get()
            post_item['crawled_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            post_item['url'] = response.urljoin(post.css('::attr(data-url)').get())
            post_item['likes'] = int(post.css('.likes::text').get() or 0)
            post_item['comments'] = int(post.css('.comments-count::text').get() or 0)
            post_item['shares'] = int(post.css('.shares::text').get() or 0)

            yield post_item

            # 如果有评论区，提取评论
            comments = post.css('.comment')
            for comment in comments:
                comment_item = CommentItem()
                comment_item['post_id'] = post_item['original_id']
                comment_item['author'] = comment.css('.comment-author::text').get()
                comment_item['content'] = comment.css('.comment-content::text').get()
                comment_item['comment_time'] = comment.css('.comment-time::text').get()
                comment_item['crawled_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                comment_item['likes'] = int(comment.css('.comment-likes::text').get() or 0)

                yield comment_item