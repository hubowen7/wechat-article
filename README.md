# 微信公众号文章抓取与筛选项目

## 项目概述
该项目旨在使用Python和Selenium从微信公众号抓取文章，并根据特定的标签和发布日期进行筛选。此工具对于需要自动化获取和筛选微信公众号内容的研究者或营销专业人士来说非常有用。

## 环境要求
- Python 3.12（作者所使用的版本）
- Selenium
- Requests
- Chrome WebDriver

## 安装步骤
1. 安装Python：
   确保您的系统中已安装Python 3.12。可以从 [Python官网](https://www.python.org/downloads/) 下载。

2. 安装依赖库：
   依赖项已在 requirements.txt 中列出，运行以下命令安装:
   ```bash
   pip install -r requirements.txt
   ```

3. 安装Chrome WebDriver：
   根据您的Chrome版本下载对应的Chrome WebDriver。请确保WebDriver的路径已添加到系统的PATH中，或在代码中指定路径。下载链接 [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/).

## 使用说明
1. **设置项目**：
   克隆或下载本项目代码到本地目录。

2. **配置参数**：
   在代码中，您可以修改以下几个关键参数：
   - `fake_id`：设置为目标公众号的唯一标识。
   - `num`：在`fetch_page(num)`函数中设置，用于指定抓取的页数。

3. **运行项目**：
   在终端或命令行窗口中，导航到包含代码的目录，并运行以下命令：
   ```bash
   python get_article.py
   ```

4. **查看结果**：
   筛选后的文章标题和链接将在命令行中打印出来。

## 功能描述
- **抓取文章**：从指定微信公众号抓取文章列表。
- **筛选文章**：根据发布日期和标签筛选文章。文章必须至少包含两个相关标签，并在最近一个月内发布。

## 注意事项
- 本项目使用了Selenium进行网页模拟访问，可能受到目标网站反爬虫策略的影响。
- 确保在使用过程中遵守相关网站的服务条款，避免过于频繁的请求。

## 贡献
欢迎对项目进行改进和优化的相关建议和贡献。您可以通过GitHub提交Pull Requests或开设Issues。

## 许可证
本项目采用MIT许可证。使用本项目之前，请确保您已阅读并同意许可证条款。

---

确保在使用本工具时遵守相关法律法规以及微信公众平台的规定。此代码仅供学习和研究使用，不得用于任何非法用途。
