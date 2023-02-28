import requests
import json
from common.unittest_report_logs import info_log
from common.read_yaml import ReadYaml


class Notes(object):
    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.userid = data["userid"]
        cls.sid = data['sid']

    # 1、查询便签列表
    @staticmethod
    def get_notes(host, sid, userid, startindex, rows):
        uri = "/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes".format(userid, startindex, rows)
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
        }
        info_log("url: {}".format(url))
        res = requests.get(url=url, headers=headers)
        return res

    # 2、上传/更新便签信息主体
    # 0表示body是便签内容，1表示body是超链接（如果便签太大，由客户端SDK上传内容到S3）
    @staticmethod
    def set_noteinfo(host, sid, userid, body):
        uri = "/v3/notesvr/set/noteinfo"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        info_log("body: {}".format(body))
        res = requests.post(url=url, headers=headers, json=body)
        return res

    # 3、上传/更新便签内容
    @staticmethod
    def set_notecontent(host, sid, userid, body):
        uri = "/v3/notesvr/set/notecontent"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        info_log("body: {}".format(body))
        res = requests.post(url=url, headers=headers, json=body)
        return res

    # 4、获取标签内容
    @staticmethod
    def get_notebody(host, sid, userid, body):
        uri = "/v3/notesvr/get/notebody"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(body))
        return res

    # 5、删除便签
    @staticmethod
    def del_notesvr(host, sid, userid, body):
        uri = "/v3/notesvr/delete"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))
        return res


