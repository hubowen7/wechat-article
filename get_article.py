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

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_article_details(article_url):
    """ 使用Selenium抓取文章的详细信息，包括标签和发布日期 """
    logging.info(f"开始抓取文章: {article_url}")
    options = Options()
    options.headless = True  # 使用无头模式
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--window-size=1920x1080")  # 指定浏览器分辨率
    service = Service(executable_path='./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(article_url)
        time.sleep(10)  # 增加等待时间以减少爬取速度，减轻服务器压力
        tags = {tag.text.strip() for tag in driver.find_elements(By.CLASS_NAME, 'article-tag__item')}
        publish_em = driver.find_element(By.ID, 'publish_time')
        publish_date_str = publish_em.text.strip() if publish_em else ''
        publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d %H:%M') if publish_date_str else None
        logging.info(f"文章抓取完成: 标签 - {tags}, 发布日期 - {publish_date}")
        return tags, publish_date
    except Exception as e:
        logging.error(f"在抓取文章信息时发生错误: {e}", exc_info=True)
    finally:
        driver.quit()

def filter_articles(articles):
    """ 根据特定条件筛选文章 """
    logging.info("开始根据特定条件筛选文章")
    filtered_articles = []
    one_month_ago = datetime.now() - timedelta(days=5)
    valid_tags = {tag.value for tag in Tag}
    for title, link in articles:
        logging.info(f"抓取并处理文章: {title}")
        tags, publish_date = fetch_article_details(link)
        time.sleep(20)  # 每次抓取后休息20秒
        # 确保日期有效且至少包含一个标签
        if publish_date and publish_date >= one_month_ago and len(tags.intersection(valid_tags)) >= 2:
            filtered_articles.append((title, link))
            logging.info(f"文章 '{title}' 符合条件并被添加到过滤列表")
        else:
            logging.info(f"文章 '{title}' 不符合条件，被跳过")
        logging.info("文章筛选完成")
    return filtered_articles

def fetch_page(num=1):
    """ 从微信公众号API抓取文章页面 """
    logging.info("开始从微信公众号API抓取文章页面")
    headers = {
        "cookie": "appmsglist_action_3296508395=card; ua_id=lTGgGdyLybxOEU7YAAAAAMJOVJrBBZLXBApnARbsQFI=; _clck=1k8cupo|1|flj|0; wxuin=15005178482107; uuid=018b1cbb7cf1176ec22d471c71ea96ff; rand_info=CAESIHL0xgA81PdNaKTTdVYOA7HekCl6TYSbEYxj4FcdDWSq; slave_bizuin=3296508395; data_bizuin=3296508395; bizuin=3296508395; data_ticket=U+vcWHVEg0+pcO0Bmoz26ny44jJXfIReAqSdTjoB5oI6sRlPRPfPoxonsIfQ9FCp; slave_sid=OWs4M05iald4ZE1GMEZJaXNrR19YMTlOcnR3SDEySmJnWlZ3R0pGZGlBak9tNUF1WUl1cXlyUWcwSW1ac1U3RjVnWEk3YU9SNURJb2lNTlE5bHZHTXZnc2ZIb2tXd3BpRFlPcjROOHp4NHhPMl9CVGhrVTh6T1RWOWF6eVMwZkVwS09NQnRZa2QwWjYxMjRm; slave_user=gh_a5060f4cf8ae; xid=d6c06582ccb272f04b4cb58e0ca2f4cf; mm_lang=zh_CN; cert=rGzj7GlVHTknNEW4BcJxk84Nrw56rphG; rewardsn=; wxtokenkey=777; _clsk=19aql5s|1715008216255|3|1|mp.weixin.qq.com/weheat-agent/payload/record",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    # 爬不同公众号只需要更改fakeid
    fake_id = 'MzIzMjA2NTg3Mw%3D%3D'
    titles_links = []
    for page_number in range(num):
        params = {
            'action': 'list_ex',
            'begin': page_number * 5,  # 为分页计算偏移量
            'count': '5',
            'fakeid': fake_id,
            'type': '9',
            'query': '',
            'token': '1132247621',
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
    articles = fetch_page(1)  # 抓取1页文章
    filtered_articles = filter_articles(articles)  # 根据条件筛选文章
    for title, link in filtered_articles:
        logging.info(f"筛选文章: {title} {link}")
        print(title, link)  # 打印筛选后的文章标题和链接
    logging.info("主程序执行结束")

if __name__ == '__main__':
    main()