import sys
import os
import json
from bs4 import BeautifulSoup
from config import MOVIE_ID, PROGRESS_FILE, JSON_FILE, CSV_FILE, RAW_COOKIE_STRING, DEFAULT_END_PAGE
from request_module import fetch_page
from storage_module import save_to_json, save_to_csv

def parse_cookie_string(cookie_string):
    """将原始的Cookie字符串解析为字典。"""
    cookies = {}
    if not cookie_string:
        return cookies
    for item in cookie_string.split('; '):
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    return cookies

def parse_douban_comments(html_content):
    """解析豆瓣电影短评的HTML内容，提取更详细的评论数据。"""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    comments = []
    comment_items = soup.select('.comment-item')
    
    if not comment_items:
        return []

    for item in comment_items:
        try:
            user_tag = item.select_one('.comment-info a')
            user = user_tag.get_text(strip=True) if user_tag else '未知用户'
            rating_tag = item.select_one('.rating')
            rating = rating_tag.get('title') if rating_tag else '无评分'
            time_tag = item.select_one('.comment-time')
            comment_time = time_tag.get_text(strip=True) if time_tag else '未知时间'
            comment_content_tag = item.select_one('.comment > p > span')
            comment_text = comment_content_tag.get_text(strip=True) if comment_content_tag else '无内容'
            
            comments.append({
                'user': user,
                'rating': rating,
                'time': comment_time,
                'content': comment_text
            })
        except Exception as e:
            print(f"解析评论时出错: {e}")
            continue
            
    return comments

def get_last_crawled_info():
    """从进度文件中读取上一次爬取的信息。"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            try:
                line = f.read().strip()
                if not line:
                    return 0, 0
                last_page, last_count = map(int, line.split(','))
                return last_page, last_count
            except (ValueError, IndexError):
                return 0, 0
    return 0, 0

def update_progress_file(page, count):
    """更新进度文件中的页码和评论数。"""
    if not os.path.exists(os.path.dirname(PROGRESS_FILE)):
        os.makedirs(os.path.dirname(PROGRESS_FILE))
    with open(PROGRESS_FILE, 'w') as f:
        f.write(f"{page},{count}")

def load_existing_data():
    """加载已有的数据文件，如果不存在则返回空列表。"""
    if os.path.exists(JSON_FILE):
        print("检测到已有数据文件，正在加载...")
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                print(f"已加载 {len(data)} 条评论。")
                return data
            except (json.JSONDecodeError, FileNotFoundError):
                print("加载数据文件失败或文件格式不正确，将重新开始。")
                return []
    return []

def run_crawler():
    """执行爬虫任务的主逻辑。"""
    login_cookies = parse_cookie_string(RAW_COOKIE_STRING)
    if not login_cookies:
        print("警告：Cookie字符串为空或无效，可能无法爬取所有评论。")
    
    all_comments = load_existing_data()
    last_page, last_count = get_last_crawled_info()
    start_page = 1
    
    if last_page > 0 and len(all_comments) == last_count:
        print(f"检测到上次爬取在第 {last_page} 页中断，已爬取 {last_count} 条评论。")
        choice = input("是否从中断处继续爬取？(y/n): ").lower()
        if choice == 'y':
            start_page = last_page + 1
            
    while True:
        print(f"当前爬取将从第 {start_page} 页开始。")
        end_page_input = input(f"请输入爬取结束页码（默认 {DEFAULT_END_PAGE}）：")
        
        end_page = int(end_page_input) if end_page_input.isdigit() else DEFAULT_END_PAGE
        
        if end_page >= start_page:
            break
        else:
            print(f"错误：结束页码({end_page})不能小于开始页码({start_page})，请重新输入。")
    
    base_url = f"https://movie.douban.com/subject/{MOVIE_ID}/comments"
    comment_counter = len(all_comments) + 1
    
    print(f"--- 正在开始爬取电影短评，从第 {start_page} 页到第 {end_page} 页 ---")

    for i in range(start_page, end_page + 1):
        start_value = (i - 1) * 20
        url = f"{base_url}?start={start_value}&limit=20&sort=new_score&status=P"
        
        print(f"正在爬取第 {i}/{end_page} 页，URL: {url}")
        
        response = fetch_page(url, cookies=login_cookies)
        
        if not response:
            print(f"第 {i} 页请求失败，程序将停止。")
            save_to_json(all_comments, os.path.basename(JSON_FILE))
            save_to_csv(all_comments, os.path.basename(CSV_FILE))
            print("所有数据已保存。")
            sys.exit()
        
        page_comments = parse_douban_comments(response.text)
        
        if not page_comments:
            print("未找到更多评论，爬取提前结束。")
            break
        
        for comment in page_comments:
            comment['id'] = comment_counter
            comment_counter += 1
        
        all_comments.extend(page_comments)
        print(f"第 {i} 页爬取成功，已获取 {len(page_comments)} 条评论。")
        
        update_progress_file(i, len(all_comments))
        
        print("-" * 20)

    print(f"爬取完成！总共获取到 {len(all_comments)} 条评论。")
    
    save_to_json(all_comments, os.path.basename(JSON_FILE))
    save_to_csv(all_comments, os.path.basename(CSV_FILE))
    print("所有数据已保存。")