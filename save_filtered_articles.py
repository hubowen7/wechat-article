import os
import csv
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_article_to_csv(article):
    """ 将符合条件的文章标题和链接写入到一个CSV文件中 """
    # 获取当前日期并格式化为所需的文件名格式
    current_date_str = datetime.now().strftime('%Y%m%d')
    file_name = f"{current_date_str}.csv"

    # 确定保存目录
    save_dir = os.path.join(os.getcwd(), 'article')

    # 如果目录不存在，则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        logging.info(f"目录 {save_dir} 不存在，已创建")

    # 确定文件路径
    file_path = os.path.join(save_dir, file_name)

    # 检查文件是否存在，若不存在则写入表头
    file_exists = os.path.isfile(file_path)

    # 写入CSV文件，使用UTF-8带BOM编码
    with open(file_path, mode='a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writerow(['标题', '链接'])
        # 写入文章数据
        writer.writerow(article)

    logging.info(f"文章已保存到文件: {file_path}")
