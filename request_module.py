import requests
import random
import time
from config import GLOBAL_REQUEST_CONFIG

# 伪装User-Agent，模拟不同的浏览器访问
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

def fetch_page(url, method='GET', headers=None, params=None, data=None, cookies=None):
    """
    通用网页请求函数，包含重试、延迟和代理功能。
    
    Args:
        url (str): 目标URL。
        method (str): 请求方法，'GET'或'POST'。
        headers (dict): 请求头。
        params (dict): URL参数。
        data (dict): POST请求数据。
        cookies (dict): 请求携带的Cookies。

    Returns:
        requests.Response: 请求成功时的响应对象，失败时返回None。
    """
    max_retries = GLOBAL_REQUEST_CONFIG['retries']
    
    # 构建请求头，并添加Referer
    selected_headers = {'User-Agent': random.choice(USER_AGENTS)}
    if headers:
        selected_headers.update(headers)
    
    # 随机选择代理IP
    proxies = {}
    if GLOBAL_REQUEST_CONFIG['proxy_list']:
        selected_proxy = random.choice(GLOBAL_REQUEST_CONFIG['proxy_list'])
        proxies = {
            'http': selected_proxy,
            'https': selected_proxy,
        }

    for i in range(max_retries):
        delay = random.uniform(GLOBAL_REQUEST_CONFIG['delay_range'][0], GLOBAL_REQUEST_CONFIG['delay_range'][1])
        time.sleep(delay)
        print(f"[{i+1}/{max_retries}] 正在请求 {url}, 延迟 {delay:.2f} 秒...")

        try:
            if method.upper() == 'GET':
                response = requests.get(
                    url,
                    headers=selected_headers,
                    params=params,
                    cookies=cookies,
                    timeout=GLOBAL_REQUEST_CONFIG['timeout'],
                    proxies=proxies,
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    headers=selected_headers,
                    data=data,
                    cookies=cookies,
                    timeout=GLOBAL_REQUEST_CONFIG['timeout'],
                    proxies=proxies,
                )
            else:
                raise ValueError("不支持的请求方法: " + method)
            
            # 检查响应状态码
            response.raise_for_status()
            
            print("请求成功！")
            return response

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if i < max_retries - 1:
                print("等待重试...")
            else:
                print("达到最大重试次数，放弃请求。")
    
    return None