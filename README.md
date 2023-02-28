# 接口自动化测试框架
..
## 技术栈
python+unittest+request+beatifulReport+jenkins

## 常用库
- time
  - 获取时间戳，传参
- json
  - json.dumps(dict) 序列化 => str
  - json.load(str) 反序列化 => dict
- random
  - 生成随机参数，比如：用户名
- pymysql
  - 快速连接并操作数据库

## 接口自动化用例设计维度
- 接口_输入
- 接口_处理
- 接口_输出

## jenkins 项目部署
- 启动脚本sh
- jenkins项目配置
- 如何安装包
- git拉取代码

## 实践总结
- 全局参数：域名、登录用户名、密码
- 构建测试套件：
  - 按测试模块执行:一个python文件就是一个模块，一个模块可以有多个测试类，一个测试类可以有多个测试用例
- 批量执行测试用例
  - 通过discover方法，批量获取测试模块中用到的方法
  ```
  testsuite = unittest.defaultTestLoader.discover(
        start_dir=DIR + '/testCase',
        pattern="test_*.py",
        top_level_dir=None
    )
  ```
- 生成测试报告
  ```
  result = BeautifulReport(test_suite)
  result.report(filename=filename, description='测试deafult报告', report_dir=DIR)
  ```
- 测试断言
  - assertEqual
  - assertTrue


## 为什么要用代码写自动化，而不用三方postman,jmeter等工具
- jmeter不够灵活，比如某些字段需要经过特定的加密处理，不能通过Jmeter直接完成
- 代码，测试数据容易控制（比如造大量数据）；可以使用加密函数对接口加密；容易扩展
- 大项目不利于团队协作

## 待解决的问题
- 接口自动化的用例粒度
  - 单接口用例
  - 场景用例
- 文件上传场景
  - pdf文件
  - 图片上传（大小、格式）
- 多线程执行测试用例
  - 报告生成？
  - 只有数据不冲突的场景，才能使用多线程技术运行测试用例。
  - 如果使用多线程同时使用相同用户名测试登陆和退出登陆，那么肯定会导致测试结果不准确。
  - 多线程测试修改同一行数据时，也会出现问题，导致测试结果不准确
  - 多线程测试删除同一个数据时，容易出现问题，导致结果不准确

- 如何测试接口并发？
  - 性能测试单独做
- 用例间传参数？
  - 第一种：定义为class的属性
  - 第二种：用例方法定义形参
- 代码覆盖率