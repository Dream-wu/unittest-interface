import unittest
from copy import deepcopy
import time
import random
import string
from common.read_yaml import ReadYaml
from business.notes import Notes
from common.unittest_report_logs import info_log

class TestNotes(unittest.TestCase):

    name = ""
    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        # print(data)
        cls.note = Notes()
        cls.baseData = data
        cls.hostname = data["hostname"]
        cls.userid = data["userid"]
        cls.sid = data['sid']

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        info_log("当前用例执行结束: {}".format(self.name))
        pass

    def testCase01_setNoteContent(self):
        """1、新增一个内容是【文本】的便签"""
        self.name = "新增普通便签"
        note_id = "".join(random.sample(string.ascii_letters + string.digits, 32))
        body = {
            "noteId": note_id,
            "title": "WZWsi7mvYPwPpkoEGtDKkA==",
            "summary": "Lu+Q4WSUN4bz21lYcf0ELyeb4atUMU1/4a/RZESeBog=",
            "body": "+hnQTX1CV6UoBQKumuk0Uh7Jx19D9m26Dq7mSnQzBN8=",
            "bodyType": 0
        }
        res = self.note.set_notecontent(self.hostname, self.sid, self.userid, body)
        info_log("新增便签返回: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue("contentUpdateTime" in res.json().keys())

        # 查询校验是否插入成功
        queryBody = {
            "noteIds": [note_id]
        }
        res2 = self.note.get_notebody(self.hostname, self.sid, self.userid, body=queryBody)
        info_log("查询{}便签返回: {}, {},".format(note_id, res2.status_code, res2.json()))
        self.assertEqual(200, res2.status_code)
        self.assertEqual(note_id, res2.json()["noteBodies"][0]['noteId'])

    def testCase02_setNoteContent(self):
        """2、新增一个内容是【超链接】的便签"""
        self.name = "新增【超链接】便签"
        note_id = "".join(random.sample(string.ascii_letters + string.digits, 32))
        body = {
            "noteId": note_id,
            "title": "WZWsi7mvYPwPpkoEGtDKkA==",
            "summary": "Lu+Q4WSUN4bz21lYcf0ELyeb4atUMU1/4a/RZESeBog=",
            "body": "https://www.baidu.com",
            "bodyType": 1
        }
        # "localContentVersion": 2,
        res = self.note.set_notecontent(self.hostname, self.sid, self.userid, body)
        info_log("新增便签返回: {},{},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        # 需要查询是否新增成功

        queryBody = {
            "noteIds": [note_id]
        }
        res2 = self.note.get_notebody(self.hostname, self.sid, self.userid, body=queryBody)
        info_log("查询{}便签返回: {}, {},".format(note_id, res2.status_code, res2.json()))
        self.assertEqual(200, res2.status_code)
        self.assertEqual(note_id, res2.json()["noteBodies"][0]['noteId'])

    # 获取首页便签列表
    def testCase03_getNotes(self, startindex=0, rows=10):
        """3、获取首页便签列表"""
        self.name = "便签列表"
        res = self.note.get_notes(self.hostname, self.sid, self.userid, startindex, rows)
        info_log("便签列表返回: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)
        self.assertTrue("webNotes" in res.json().keys())

    def testCase04_del_notesvr(self):
        """4、删除一个已存在的便签"""
        body ={
            "noteId": "24"
        }
        res = self.note.del_notesvr(self.hostname, self.sid, self.userid, body)
        info_log("删除一个已存在的标签: {}, {},".format(res.status_code, res.json()))
        self.assertEqual(200, res.status_code)




