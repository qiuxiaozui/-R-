**罗皓辉的R语言课程期末项目报告**  
项目名称：股票数据爬取与可视化分析系统

一、项目概述  
本项目是一个结合Python网络爬虫与R语言可视化的股票数据分析系统。通过爬取新浪财经的股票实时数据及股吧评论，利用R语言生成交互式图表和词云，实现多维度的股票分析与可视化展示。项目分为数据采集（Python）和可视化（R）两大模块，体现了多语言协作的工程实践能力。

二、模块结构与功能说明  
**1. 数据采集模块（Python）**  
*final_main.py（主控程序）*
功能：协调整个流程，包括用户输入、股票数据爬取、评论链接抓取、内容提取及调用R脚本生成可视化。
  
*`check_id.py`（股票代码转换器）*
功能：基于`akshare`库，实现股票名称与代码的互查，支持A股、港股、美股市场。  
输入输出：  
`get_stock_code()`：输入名称与市场，返回股票代码。  
`get_stock_name()`：输入代码与市场，返回股票名称。 

*`get_cookie.py`（反爬Cookie生成器）*
功能：动态生成模拟用户行为的Cookie，包括随机IP、时间戳、会话状态等，用于绕过新浪财经的反爬机制。  
核心类：`CookieGenerator`类通过随机参数构造请求头，提升爬虫隐蔽性。  

*`get_comments.py`与`get_page_data.py`（评论数据抓取）*
功能：  
异步抓取股吧评论链接（`get_comments.py`）。  
同步提取评论正文内容（`get_page_data.py`）。  
技术点：使用`BeautifulSoup`解析HTML，`aiohttp`实现异步并发请求。  

**2. 可视化模块（R语言）**  
*`main.R`（可视化脚本）*
功能：读取爬取的JSON数据，生成交互式HTML报表，包含以下图表：  
1.成交量热图：展示交易日内每10分钟的成交量分布。  
2. 价格走势图：对比实时价格与移动均价。  
3. 成交量柱状图：实时成交量分布。  
4. 词云图：从股吧评论中提取高频关键词并可视化。  

三、工作流程  
1. 用户输入：运行`final_main.py`后，用户选择输入股票代码或名称，并指定保存路径（默认`result`文件夹）。  
2.数据爬取：  
调用`get_stock_data()`获取股票实时数据（JSON格式）。  
异步抓取股吧前5页评论链接，提取文章内容并保存为`comments.json`。  
3. 可视化生成：通过`rpy2`调用R脚本`main.R`，读取JSON数据并生成包含4张图表的HTML报表。
tips:
控制台飘红时正常情况，和异步进程初始化，异步进程关闭和R语言控制台版本提示有关（python和R的特性吧）

四、运行环境  
- Python依赖库：`akshare` `rpy2` `aiohttp` `BeautifulSoup` `json` `requests`...  
- R依赖库：`plotly` `wordcloud2` `jiebaR`...
- 环境配置：
- R:需安装R语言环境（推荐4.4.3，旧版本依赖包可能会出问题）并正确设置`R_HOME`路径（Windows示例：`C:/Program Files/R/R-4.4.3`，系统路径和path都检查一下，实在不行就在main.py中放开并修改硬编码R路径的代码行），
- python: 需安装python语言环境（推荐python3.10以上）并正确设置`python`系统路径(旧版本异步进程写法不同)
  
五、开发者运行环境
(https://github.com/user-attachments/assets/9b98c789-fce9-463d-9be0-2e9922f8fbcb)

