# ================== 爬虫配置 ==================

# 电影ID，例如《肖申克的救赎》的ID
MOVIE_ID = '1292052'

# 豆瓣登录Cookie
RAW_COOKIE_STRING = '''
# 替换成你的Cookie
'''

# 爬取结束页数默认值
DEFAULT_END_PAGE = 20

# 文件路径配置
PROGRESS_FILE = 'data/progress.txt'
JSON_FILE = 'data/douban_comments.json'
CSV_FILE = 'data/douban_comments.csv'

# 请求模块的全局配置，包括代理和User-Agent
GLOBAL_REQUEST_CONFIG = {
    'timeout': 10,
    'retries': 3,
    'delay_range': (1, 3), # 随机延迟时间
    'proxy_list': [        # 代理 IP 列表，可按需添加
        # 'http://user:password@ip:port',
    ]
}

# ============================================