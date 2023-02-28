import os
import sys

import yaml
from main import Environ


class ReadYaml(object):
    def __init__(self, filename):
        # 切换环境变量
        # test测试环境
        # pre预发布环境

        # 拼接定位到data文件夹
        self.filepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + Environ)+"/"+filename

    def get_yaml_data(self):
        with open(self.filepath, "r", encoding="utf-8")as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)


class ReadYaml_anjiekou(object):
    def __init__(self, filename):
        # 拼接定位到data文件夹
        self.filepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + r"/data")+"/"+filename

    def get_yaml_data(self):
        with open(self.filepath, "r", encoding="utf-8")as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)


if __name__ == '__main__':
    main_data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
    sid = main_data['host']
    print(sid)


