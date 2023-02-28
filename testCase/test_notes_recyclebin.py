import unittest
from copy import deepcopy
import time
import random
import string
from common.read_yaml import ReadYaml
from business.notes_recyclebin import NotesRecyclebin
from common.unittest_report_logs import info_log


class TestNotesRecyclebin(unittest.TestCase):
    name = ""

    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.note = NotesRecyclebin()
        print("notes:{}".format(type(cls.note)))
        cls.baseData = data
        cls.hostname = data["hostname"]
        cls.userid = data["userid"]
        cls.sid = data['sid']

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        info_log("当前用例执行结束: {}".format(self.name))
        pass

    def testCase09_get_invalid_notes(self):
        """9、查看回收站下便签"""
        name = "查看回收站下标签"
        body = {
            "startIndex": 0,
            "rows": 50,
        }
        res = self.note.get_invalid_notes(self.hostname, self.sid, self.userid, body['startIndex'], body['rows'])
        info_log("查看回收站下便签: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue('responseTime' in res.json().keys())

    def testCase10_user_notes(self):
        """10、恢复回收站下便签"""
        name = "恢复回收站下标签"
        noteIds = ['24']
        res = self.note.user_notes(self.hostname, self.sid, self.userid, noteIds=noteIds)
        info_log("恢复回收站下便签: {}, {},".format(res.status_code, res))
        self.assertEqual(200, res.status_code)

    def testCase11_cleanrecyclebin(self):
        """11、删除/清空回收站便签"""
        name = "删除回收站下标签"
        noteIds = ['-1']
        res = self.note.cleanrecyclebin(self.hostname, self.sid, self.userid, noteIds=noteIds)
        info_log("清空回收站下便签: {},{},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
