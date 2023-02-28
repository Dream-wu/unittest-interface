import unittest
from copy import deepcopy
from common.read_yaml import ReadYaml
from business.v1_group_report import V1GroupReport
from business.v1_device import V1Device
from common.unittest_report_logs import info_log, error_log
import warnings


class CallBack(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.sid1 = data["sid1"]
        cls.sid2 = data["sid2"]
        cls.userId1 = data["userId1"]
        cls.userId2 = data["userId2"]
        cls.host = data["host"]
        cls.v1gr = V1GroupReport()
        cls.v1d = V1Device()
        cls.ak = data["device_ak"]
        cls.sk = data["device_sk"]
        cls.register_base = {
            "identify_info": {
                "app_id": "wps-office",
                "user_id": "11",
                "device_id": "device_id",
                "device_name": "device_id"
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        cls.group_report_base = {
            "identify_info": {
                "app_id": "wps-office",
                "user_id": "111",
                "device_id": "device_id"
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        cls.group_report_list_base = {
            "identify_info": {
                "app_id": "wps-office",
                "user_id": "11",
                "device_id": "device_id"
            },
            "group_type": [1, 2, 3],
            "location": {"location_radius": 10}
        }
        cls.delete_group_report_base = {
            "identify_info": {
                "app_id": "wps-office",
                "user_id": "11",
                "device_id": "device_id"
            }
        }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testCase01_major(self):
        """用户A注册设备、用户B注册设备、用户A上报设备、用户B上报设备、用户A查附近、用户B退出上报设备、用户A查附近、用户A用户B删除设备信息"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        body["identify_info"]["device_name"] = device_id

        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        body["identify_info"]["device_name"] = device_id2

        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = deepcopy(self.group_report_list_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
        self.assertEqual(str(self.userId2), res.json()["data"]["members"][0]["user_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_name"])
        self.assertEqual(app_id, res.json()["data"]["members"][0]["app_id"])
        self.assertEqual(1, len(res.json()["data"]["members"]))

        info_log("用户2退出上报接口")
        body = deepcopy(self.delete_group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.delete_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = deepcopy(self.group_report_list_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json()["data"]["members"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase02_cookie_check(self):
        """取消上报接口(v1/group/report):cookie缺失"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        body["identify_info"]["device_name"] = device_id

        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        body["identify_info"]["device_name"] = device_id2

        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2退出上报接口")
        body = deepcopy(self.delete_group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.delete_v1_group_report(self.host, body, "pop", self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(403, res.status_code)
        self.assertEqual(20001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase03_cookie_check(self):
        """取消上报接口(v1/group/report):cookie越权"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        body["identify_info"]["device_name"] = device_id

        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        body["identify_info"]["device_name"] = device_id2

        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2退出上报接口")
        body = deepcopy(self.delete_group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.delete_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase04_repeat_exit(self):
        """重复退出上报"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        body["identify_info"]["device_name"] = device_id

        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = deepcopy(self.register_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        body["identify_info"]["device_name"] = device_id2

        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = deepcopy(self.group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = deepcopy(self.group_report_list_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
        self.assertEqual(str(self.userId2), res.json()["data"]["members"][0]["user_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_name"])
        self.assertEqual(app_id, res.json()["data"]["members"][0]["app_id"])
        self.assertEqual(1, len(res.json()["data"]["members"]))

        info_log("用户2退出上报接口")
        body = deepcopy(self.delete_group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.delete_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2退出上报接口")
        body = deepcopy(self.delete_group_report_base)
        body["identify_info"]["user_id"] = str(self.userId2)
        body["identify_info"]["device_id"] = device_id2
        res = self.v1gr.delete_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = deepcopy(self.group_report_list_base)
        body["identify_info"]["user_id"] = str(self.userId1)
        body["identify_info"]["device_id"] = device_id
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json()["data"]["members"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])