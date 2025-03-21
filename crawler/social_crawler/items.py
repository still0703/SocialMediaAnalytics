import scrapy

class PostItem(scrapy.Item):
    original_id = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    post_time = scrapy.Field()
    crawled_time = scrapy.Field()
    url = scrapy.Field()
    likes = scrapy.Field()
    comments = scrapy.Field()
    shares = scrapy.Field()

class CommentItem(scrapy.Item):
    post_id = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    comment_time = scrapy.Field()
    crawled_time = scrapy.Field()
    likes = scrapy.Field()