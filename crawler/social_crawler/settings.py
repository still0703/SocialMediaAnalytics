BOT_NAME = "social_crawler"

SPIDER_MODULES = ["social_crawler.spiders"]
NEWSPIDER_MODULE = "social_crawler.spiders"

# 启用管道
ITEM_PIPELINES = {
   'social_crawler.pipelines.DatabasePipeline': 300,
}

# 设置用户代理
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# 禁止遵循robots.txt (仅用于测试，实际爬取时应尊重robots.txt规则)
ROBOTSTXT_OBEY = False

# 设置下载延迟，避免请求过于频繁
DOWNLOAD_DELAY = 0.5

# 启用日志
LOG_LEVEL = 'INFO'