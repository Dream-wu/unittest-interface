import requests
import json
from common.unittest_report_logs import info_log
from common.read_yaml import ReadYaml

class NotesGroup(object):
    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.userid = data["userid"]
        cls.sid = data['sid']

    # 获取分组列表
    @staticmethod
    def get_notegroup(host, sid, userid, body):
        uri = "/v3/notesvr/get/notegroup"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, json=body)
        return res

    # 新增分组
    @staticmethod
    def set_notegroup(host, sid, userid, body):
        uri = "/v3/notesvr/set/notegroup"
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

    # 查看分组下便签
    # groupId	string	required	分组id
    # startIndex	int	optional	起始索引,不传默认为0
    # rows	int	optional	数据行数，不传默认为50
    @staticmethod
    def get_group(host, sid, userid, body):
        uri = "/v3/notesvr/web/getnotes/group"
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

    # 删除分组
    # groupId	string	required	分组id
    @staticmethod
    def del_notegroup(host, sid, userid, body):
        uri = "/v3/notesvr/delete/notegroup"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, json=body)
        return res

    # 10、查看日历下便签
    # remindStartTime	long	required	month开始的时间戳
    # remindEndTime	long	required	month结束的时间戳
    # startIndex	int	required	起始索引
    # rows	int	required	读取行数
    @staticmethod
    def get_remind(host, sid, userid, body):
        uri = "/v3/notesvr/web/getnotes/remind"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid={}'.format(sid),
            "X-user-key": str(userid)
        }
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, json=body)
        return res
