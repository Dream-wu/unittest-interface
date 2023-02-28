import requests
import json
from common.unittest_report_logs import info_log
from common.read_yaml import ReadYaml


class NotesRecyclebin(object):
    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.userid = data["userid"]
        cls.sid = data['sid']

    # 查看回收站下便签列表
    # userid	long	required	userid
    # startIndex	int	required	起始索引
    # rows	int	required	读取行数
    @staticmethod
    def get_invalid_notes(host, sid, userid, startIndex=0, rows=50):
        uri = "/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes".format(userid, startIndex, rows)
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        body = {
            "userid": userid,
            "startIndex": startIndex,
            "rows": rows
        }
        res = requests.get(url=url, headers=headers, json=body)
        return res

    # 恢复回收站的便签
    # userId	long	required	userid
    # noteIds	string[]	required	恢复的便签i
    @staticmethod
    def user_notes(host, sid, userid, noteIds=[]):
        uri = "/v3/notesvr/user/{}/notes".format(userid)
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        body = {
            "userId": userid,
            "noteIds": noteIds
        }
        res = requests.patch(url=url, headers=headers, json=body)
        return res

    # 13、删除/清空回收站便签
    # noteIds	string[]	required	恢复的便签id
    @staticmethod
    def cleanrecyclebin(host, sid, userid, noteIds=[]):
        uri = "/v3/notesvr/cleanrecyclebin"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        body = {
            "noteIds": noteIds
        }
        info_log("url: {}".format(url))
        info_log("body: {}".format(body))
        res = requests.post(url=url, headers=headers, json=body)
        return res
