# hotel-data-crawler
 给公司在apollo上爬取指定员工信息

## 环境准备
1. 配置浏览器调试端口
   - 创建Chrome或Edge浏览器的快捷方式
   - 在目标属性中添加调试端口参数：
     ```
     "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
     ```
   - 使用此快捷方式打开浏览器并登录apollo系统
2. 下载需要的包：
    pip install DrissionPage==4.1.0.12
    pip install pandas

## 数据获取流程

### 1. 爬取基础数据
- 将要爬的公司放在酒店英文名.txt
- 运行 `apollo爬虫.py` 
  - 首先执行"测试获取所有公司地址"获取查询地址
  - 然后执行"多进程爬取"根据这些公司地址，爬所有公司的所有员工信息
  - 数据将保存在当前目录下的`csv`文件夹中

### 2. 邮箱处理
- 运行 `analyze_email_patterns.py` 分析邮件格式 （传csv文件目录）
  - 在目录下生成 `result_analyze_email.json`  （统计每个公司下各个员工的邮件域名，命名情况）
- 运行 `generate_missing_emails.py` 补充缺失邮箱 （根据比例最大的域名和命名情况进行填补）
  - 根据分析结果生成新的CSV文件
  - 输出位置：`更新后的文件`目录

### 3. 数据整合
- 运行 `filter_and_merge.py` 过滤出所需要的职位，并且合并所有CSV文件为一个csv文件（传csv文件目录）

### 4. 总经理信息补充
- 运行 `search_general_manager.py` 搜索总经理信息 （传最终一个csv文件）
  - 生成 `经理填补日志.txt`
- 运行 `经理填补日志.py` 更新CSV文件（传最终一个csv文件）
  - 将总经理信息填补到最终数据中
