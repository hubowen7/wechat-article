# -*- coding: utf-8 -*-
import time
from tags import Tag
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from fake_ids import PublicAccount
from save_filtered_articles import save_article_to_csv

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_article_details(article_url):
    """ 使用Selenium抓取文章的详细信息，包括标签和发布日期 """
    logging.info(f"开始抓取文章: {article_url}")
    options = Options()
    options.headless = True  # 使用无头模式
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--window-size=1920x1080")  # 指定浏览器分辨率
    service = Service(executable_path=r'C:\Users\Bowen\PycharmProjects\wechat-article\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(article_url)
        time.sleep(10)  # 增加等待时间以减少爬取速度，减轻服务器压力
        tags = {tag.text.strip() for tag in driver.find_elements(By.CLASS_NAME, 'article-tag__item')}
        publish_em = driver.find_element(By.ID, 'publish_time')
        publish_date_str = publish_em.text.strip() if publish_em else ''

        # 尝试解析第一种格式
        publish_date = None
        try:
            publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            # 如果失败，则尝试解析第二种格式
            try:
                publish_date = datetime.strptime(publish_date_str, '%Y年%m月%d日 %H:%M')
            except ValueError:
                logging.error(f"无法解析日期格式: {publish_date_str}")

        logging.info(f"文章抓取完成: 标签 - {tags}, 发布日期 - {publish_date}")
        return tags, publish_date
    except Exception as e:
        logging.error(f"在抓取文章信息时发生错误: {e}", exc_info=True)
        return None, None  # 避免解包错误
    finally:
        driver.quit()

def filter_articles(articles):
    """ 根据特定条件筛选文章 """
    logging.info("开始根据特定条件筛选文章")
    filtered_articles = []
    one_month_ago = datetime.now() - timedelta(days=30)
    valid_tags = {tag.value for tag in Tag}
    for title, link in articles:
        logging.info(f"抓取并处理文章: {title}")
        tags, publish_date = fetch_article_details(link)
        time.sleep(20)  # 每次抓取后休息20秒
        # 检查标题是否包含任何有效标签
        title_contains_valid_tag = any(tag in title for tag in valid_tags)
        # 确保日期有效且至少包含一个标签或标题包含有效标签
        if publish_date and publish_date >= one_month_ago and (
                len(tags.intersection(valid_tags)) >= 1 or title_contains_valid_tag):
            filtered_articles.append((title, link))
            logging.info(f"文章 '{title}' 符合条件并被添加到过滤列表")
            # 将符合条件的文章立即写入到CSV文件
            save_article_to_csv((title, link))
        else:
            logging.info(f"文章 '{title}' 不符合条件，被跳过")
        logging.info("文章筛选完成")
    return filtered_articles

def fetch_page(account, num):
    """ 从微信公众号API抓取文章页面 """
    logging.info("开始从微信公众号API抓取文章页面")
    headers = {
        "cookie": "appmsglist_action_3296508395=card; pgv_pvid=3687186048; pac_uid=0_363d358634f8e; iip=0; _qimei_uuid42=17b060e0d1f10046c43c587956fc12227bbd71505d; _qimei_fingerprint=46dd3f238152da3f9a137eb14d04c768; _qimei_q36=; _qimei_h38=4abb54dcc43c587956fc12220200000a417b06; ua_id=GLYwNjR0NzgdUMmjAAAAAErcxC-gq6OQm5G3M2zg2YQ=; _clck=u91a5e|1|fnf|0; wxuin=20888773803529; uuid=f5d7cabc8edd5d6187f9040e4ac4cb30; rand_info=CAESINC1hjilGk4tgC+qWpBru0YcRRmr3spS0Y2IeLjd2QON; slave_bizuin=3296508395; data_bizuin=3296508395; bizuin=3296508395; data_ticket=M1vjX9qAxxwH64J1vuPhKn4SOUMxH3S4g6TeSnD8zyeVzrBz/oyYPs/i7E4LOBRK; slave_sid=MW82MlY0YU12QkR0azc3UW9nYmpHdVFyMUJMd2VMcHROOXhWd0s4UnJjbEhTaHI4UjV5UG9qMWx3QndRVEdkRk5xQUw4MkU2RGFZYXB4aHUxVEV1V3FyM2JaUm54SkNWV3RKVnFNU1gzZVV3X1J5eDZaYnl5c1VaVlhWYnFvNnJUa1J3R1JsSzRxdjF4a3U4; slave_user=gh_a5060f4cf8ae; xid=3aa4b86e1d89d4da103513c3d1327b89; mm_lang=zh_CN; cert=Tto82yIXPi_FChucAmXlfxNkY0ta4JRt; _clsk=1au4f3f|1720889455685|4|1|mp.weixin.qq.com/weheat-agent/payload/record",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    # 爬不同公众号只需要更改fakeid
    fake_id = account.value
    titles_links = []
    for page_number in range(num):
        params = {
            'action': 'list_ex',
            'begin': page_number * 5,  # 为分页计算偏移量
            'count': '5',
            'fakeid': fake_id,
            'type': '9',
            'query': '',
            'token': '80741581',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        response = requests.get(url, headers=headers, params=params)
        logging.info(f"第 {page_number} 页: 请求成功，状态码 200")
        if response.status_code == 200:
            try:
                data = response.json()
                if 'app_msg_list' in data:
                    for article in data['app_msg_list']:
                        titles_links.append((article['title'], article['link']))
                else:
                    logging.warning(f"第 {page_number} 页: 'app_msg_list' 键不存在于响应中")
            except ValueError:
                logging.error(f"第 {page_number} 页: JSON解码失败")
        else:
            logging.error(f"第 {page_number} 页: HTTP错误 {response.status_code}")
    return titles_links

def main():
    logging.info("主程序开始执行")
    for account in PublicAccount:
        logging.info(f"处理公众号: {account.name}")
        articles = fetch_page(account, 5)
        logging.info(f"获取到的文章数量: {len(articles)}")
        filter_articles(articles)  # 调用 filter_articles 来筛选文章
    logging.info("主程序执行结束")

if __name__ == '__main__':
    main()