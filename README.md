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
    pip install DrissionPage pandas

## 数据获取流程

### 1. 爬取基础数据
- 运行 `apollo爬虫.py`
  - 首先执行"测试获取所有公司地址"获取查询地址
  - 然后执行"多进程爬取"获取详细信息
  - 数据将保存在当前目录下的`csv`文件夹中

### 2. 邮箱处理
- 运行 `analyze_email_patterns.py` 分析邮件格式
  - 生成 `result_analyze_email.json`
- 运行 `generate_missing_emails.py` 补充缺失邮箱
  - 根据分析结果生成新的CSV文件
  - 输出位置：`更新后的文件`目录

### 3. 数据整合
- 运行 `filter_and_merge.py` 合并所有CSV文件为一个csv文件

### 4. 总经理信息补充
- 运行 `search_general_manager.py` 搜索总经理信息
  - 生成 `经理填补日志.txt`
- 运行 `经理填补日志.py` 更新CSV文件
  - 将总经理信息填补到最终数据中
