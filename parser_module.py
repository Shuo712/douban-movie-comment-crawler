from bs4 import BeautifulSoup

def parse_html_to_list(html_content):
    """
    Args:
        html_content (str): 从请求模块获取的HTML字符串。

    Returns:
        list: 包含字典的列表，每个字典代表一个数据项。
    """
    if not html_content:
        print("解析失败：HTML内容为空。")
        return []

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 这里我们使用一个假设的HTML结构进行演示。
    # 在实际使用中，你需要根据目标网站的HTML结构来修改这里的选择器。
    
    # 假设我们要爬取一个博客列表，每个列表项包含标题和链接
    data_list = []
    articles = soup.select('div.article-list-item') # 使用CSS选择器
    
    if not articles:
        print("未找到匹配的文章列表项。")
        return []

    for article in articles:
        try:
            # 提取标题
            title_tag = article.select_one('h2.title a')
            title = title_tag.get_text(strip=True) if title_tag else "无标题"
            
            # 提取链接
            link_tag = article.select_one('h2.title a')
            link = link_tag.get('href') if link_tag and link_tag.get('href') else "无链接"
            
            # 提取摘要（如果存在）
            summary_tag = article.select_one('p.summary')
            summary = summary_tag.get_text(strip=True) if summary_tag else "无摘要"
            
            # 将提取的数据存入字典
            data_item = {
                'title': title,
                'link': link,
                'summary': summary
            }
            data_list.append(data_item)
            
        except Exception as e:
            print(f"数据解析过程中出现错误：{e}")
            continue

    return data_list