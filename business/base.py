import unittest
import requests

from common.read_yaml import ReadYaml


class Base:
    @classmethod
    def setUpClass(cls):
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        # cls.userid = data["userid"]
        cls.host = data['host']

    @staticmethod
    def login(host, username, pwd):
        """登录"""
        url = host + "/login"
        headers = {
            'Content-Type': 'application/json',
        }
        body = {
            username: username,
            pwd: pwd
        }
        return requests.post(url=url, headers=headers, json=body)

    @staticmethod
    def file_upload(host, files=[]):
        """文件上传"""
        # files:[('filename', fileobj)]
        url = host + "/upload"
        headers = {
            'Content-Type': 'application/form-multipart',
        }
        return requests.post(url=url, headers=headers, files=files)
