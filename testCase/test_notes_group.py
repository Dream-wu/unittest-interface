import unittest
from copy import deepcopy
import time
import random
import string
from common.read_yaml import ReadYaml
from business.notes_group import NotesGroup
from common.unittest_report_logs import info_log

class TestNotesGroup(unittest.TestCase):

    name = ""
    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        # print(data)
        cls.note = NotesGroup()
        cls.baseData = data
        cls.hostname = data["hostname"]
        cls.userid = data["userid"]
        cls.sid = data['sid']

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        info_log("当前用例执行结束: {}".format(self.name))
        pass

    def testCase05_setNotegroup(self):
        """5、新增一个分组"""
        body = {
            "groupId": "1",
            "groupName": "分组名称"
        }
        res = self.note.set_notegroup(self.hostname, self.sid, self.userid, body)
        info_log("新增一个分组: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue('updateTime' in res.json().keys())

    def testCase06_get_group(self):
        """6、查看分组下便签"""
        body = {
            "groupId": "1",
            "startIndex": 0,
            "rows": 50
        }
        res = self.note.get_group(self.hostname, self.sid, self.userid, body)
        info_log("查看分组下标签: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue('webNotes' in res.json().keys())

    def testCase07_del_notegroup(self):
        """7、删除一个分组"""
        body = {
            "groupId": "1",
        }
        res = self.note.del_notegroup(self.hostname, self.sid, self.userid, body)
        info_log("删除一个分组: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue('responseTime' in res.json().keys())


    def testCase08_del_notegroup(self):
        """8、查看日历下便签"""
        # 时间戳
        start = time.time() - 60*60*1000*24
        # print(start.strftime("%Y-%m-%d %X"))
        body = {
            "remindStartTime": start,
            "remindEndTime": time.time(),
            "startIndex": 0,
            "rows": 50,
        }
        res = self.note.get_remind(self.hostname, self.sid, self.userid, body)
        info_log("查看日历下便签: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue('responseTime' in res.json().keys())




