from crawler import run_crawler

def main():
    """
    程序的入口点，负责启动爬虫任务。
    """
    print("--- 豆瓣电影短评爬虫启动 ---")
    run_crawler()
    print("--- 程序已退出 ---")

if __name__ == "__main__":
    main()