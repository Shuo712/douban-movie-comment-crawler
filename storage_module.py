import json
import csv
import os

def save_to_json(data, filename):
    """
    将数据保存到 JSON 文件。
    
    Args:
        data (list): 待保存的数据列表。
        filename (str): 文件名。
    """
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    
    # 确保 data 目录存在
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已成功保存到 {file_path}")

def save_to_csv(data, filename):
    """
    将数据保存到 CSV 文件。
    
    Args:
        data (list): 待保存的数据列表。
        filename (str): 文件名。
    """
    if not data:
        return
        
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    
    # 确保 data 目录存在
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    keys = data[0].keys()
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        print(f"数据已成功保存到 {file_path}")