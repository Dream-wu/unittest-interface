import unittest
import json
import time
from common.read_yaml import ReadYaml
from business.v1_group_report import V1GroupReport
from business.v1_device import V1Device
from common.unittest_report_logs import info_log, error_log


class CallBack(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @unittest.skip("demo")
    def testCase00_major(self):
        """上报接口(v1/group/report):identify_info 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase01_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])
        self.assertEqual('invalid identify_info', res.json()["msg"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase02_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info app_id 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                # "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase03_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info app_id 非枚举值"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": "abcdefg",
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase04_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info app_id null"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": None,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase05_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info app_id int"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": 123,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase06_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info user_id 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                # "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase07_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info user_id 不存在的值"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(12341231231231),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase08_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info user_id int"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": self.userId1,
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase09_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info device_id 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                # "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase10_api_input_identify_info_check(self):
        """上报接口(v1/group/report):identify_info device_id 非枚举"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": "asdasdasd"
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase11_api_input_location_check(self):
        """上报接口(v1/group/report):location 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            # "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase12_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 未必填 取默认值"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                # "latitude": 13.23232,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase13_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 0"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": 0,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase14_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 85"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": 85,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase15_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 -85"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": -85,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase16_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 20.555555"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": 20.555555,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase17_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 20.5555555555555"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": 20.5555555555555,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase18_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 -86"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": -86,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase19_api_input_location_check(self):
        """上报接口(v1/group/report):location latitude 边界值 86"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {
                "latitude": 86,
                "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase20_api_input_location_check(self):
        """上报接口(v1/group/report):location longitude 边界值 0"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 0},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase21_api_input_location_check(self):
        """上报接口(v1/group/report):location longitude 边界值 180"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 180},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase22_api_input_location_check(self):
        """上报接口(v1/group/report):location longitude 边界值 -180"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": -180},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase23_api_input_location_check(self):
        """上报接口(v1/group/report):location longitude 边界值 181"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 181},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase24_api_input_location_check(self):
        """上报接口(v1/group/report):location longitude 边界值 -181"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": -181},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase25_api_input_network_check(self):
        """上报接口(v1/group/report):network 未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            # "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase26_api_input_network_check(self):
        """上报接口(v1/group/report):network lan未必填"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            "network": {
                # "lan": "127.0.0.1/24"
            },
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase27_api_input_network_check(self):
        """上报接口(v1/group/report):network lan abc"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            "network": {
                "lan": "abc"
            },
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    @unittest.skip("long time")
    def testCase28_api_input_expire_check(self):
        """上报接口(v1/group/report):expire 未必填，取默认值5min"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2,
                "device_name": device_id2
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            # "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 600000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("等待280s")
        time.sleep(280)
        info_log("用户2查附近")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "group_type": [1, 2, 3],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
        self.assertEqual(str(self.userId1), res.json()["data"]["members"][0]["user_id"])
        self.assertEqual(device_id, res.json()["data"]["members"][0]["device_id"])
        self.assertEqual(device_id, res.json()["data"]["members"][0]["device_name"])
        self.assertEqual(app_id, res.json()["data"]["members"][0]["app_id"])
        self.assertEqual(1, len(res.json()["data"]["members"]))

        info_log("等待30s")
        time.sleep(30)
        info_log("用户2查附近")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "group_type": [1, 2, 3],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid2, self.ak, self.sk)
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

    def testCase29_api_input_cookie_check(self):
        """上报接口(v1/group/report):cookie check"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            "network": {
                "network": {"lan": "127.0.0.1/24"},
            },
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, "", self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(403, res.status_code)
        self.assertEqual(20001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase30_api_input_cookie_check(self):
        """上报接口(v1/group/report):cookie 不携带"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            "network": {
                "network": {"lan": "127.0.0.1/24"},
            },
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, "pop", self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(403, res.status_code)
        self.assertEqual(20001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase31_api_input_cookie_check(self):
        """上报接口(v1/group/report):cookie 越权"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 13},
            "network": {
                "network": {"lan": "127.0.0.1/24"},
            },
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4001, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase32_repeat_callback(self):
        """重复上报设备信息，第二次上报信息覆盖第一次上报信息"""
        info_log("用户1注册设备")
        app_id = "wps-office"
        device_id = "test001"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id,
                "device_name": device_id
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2注册设备")
        device_id2 = "test002"
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2,
                "device_name": device_id2
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0"},
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }
        res = self.v1d.post_v1_device_register(self.host, body, self.sid2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户2上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "group_type": [1, 2, 3],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
        self.assertEqual(str(self.userId2), res.json()["data"]["members"][0]["user_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_name"])
        self.assertEqual(app_id, res.json()["data"]["members"][0]["app_id"])
        self.assertEqual(1, len(res.json()["data"]["members"]))

        info_log("用户2再次上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 20.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 60000
        }
        res = self.v1gr.post_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("用户1查附近")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId1),
                "device_id": device_id
            },
            "group_type": [1, 2, 3],
            "location": {"location_radius": 10}
        }
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
