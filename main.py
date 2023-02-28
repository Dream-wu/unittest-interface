import unittest
# from tools.HTMLTestRunner import HTMLTestRunner
import time
import os
from BeautifulReport import BeautifulReport
import datetime
"""切换环境"""

# 使用哪个环境打开哪个环境
# 测试环境
# Environ = "/conf/Offline/"
# 线上环境
Environ = "/conf/Online/"
# 预发布环境
# Environ = "/configs/uat"


baseDir = os.path.dirname(__file__)
DIR = os.path.dirname(os.path.abspath(__file__))


def run(test_suite):
    # 定义输出的文件位置和名字
    # now = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试deafult报告', report_dir=DIR)


if __name__ == "__main__":

    # discover方法执行测试套件
    start_time = datetime.datetime.now()
    print("start time : {}".format(datetime.datetime.now()))
    testsuite = unittest.defaultTestLoader.discover(
        start_dir=DIR + '/testCase',
        pattern="test_*.py",
        top_level_dir=None
    )
    # for i in range(testsuite.countTestCases()):
    run(testsuite)
    end_time = datetime.datetime.now()
    print("end time : {}".format(end_time))
    print("use time : {}".format(end_time-start_time))
    print(testsuite.countTestCases())



