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

    def testCase01_major(self):
        """用户A注册设备、用户B注册设备、用户A上报设备、用户B上报设备、用户A查附近、用户B退出上报设备、用户A查附近、用户A用户B删除设备信息"""
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

        info_log("用户2退出上报接口")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            }
        }
        res = self.v1gr.delete_v1_group_report(self.host, body, self.sid2, self.ak, self.sk)
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

    def testCase02_api_input_group_type_check(self):
        """上报接口(v1/group/report/list):group_type 非枚举值"""
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
            "group_type": [4],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase03_api_input_group_type_check(self):
        """上报接口(v1/group/report/list):group_type 包含非枚举值"""
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
            "group_type": [1, 4],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase04_api_input_group_type_check(self):
        """上报接口(v1/group/report/list):group_type 空list"""
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
            "group_type": [],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase05_api_input_group_type_check(self):
        """上报接口(v1/group/report/list):group_type string"""
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
            "group_type": ["1"],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase06_api_input_group_type_check(self):
        """上报接口(v1/group/report/list):group_type string"""
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
            "group_type": 1,
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase07_api_input_location_check(self):
        """上报接口(v1/group/report/list):location 边界值101"""
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
            "location": {"location_radius": 101}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase08_api_input_location_check(self):
        """上报接口(v1/group/report/list):location 边界值100"""
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
            "location": {"location_radius": 100}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase09_api_input_location_check(self):
        """上报接口(v1/group/report/list):location 边界值0"""
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
            "location": {"location_radius": 0}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase10_api_input_location_check(self):
        """上报接口(v1/group/report/list):location 边界值-1"""
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
            "location": {"location_radius": -1}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase11_api_input_location_check(self):
        """上报接口(v1/group/report/list):location 未必填"""
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
            "group_type": [1, 2, 3]
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(400, res.status_code)
        self.assertEqual(4000, res.json()["code"])

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase12_api_input_cookie_check(self):
        """上报接口(v1/group/report/list):cookie缺失"""
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
            "location": {"location_radius": 100}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, "pop", self.ak, self.sk)
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

    def testCase13_api_input_cookie_check(self):
        """上报接口(v1/group/report/list):cookie越权"""
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
            "location": {"location_radius": 100}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid2, self.ak, self.sk)
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

    def testCase14_expire_check(self):
        """上报接口(v1/group/report/list):expire=3000，等待4s后过期"""
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
            "expire": 3000
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
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
        self.assertEqual(str(self.userId2), res.json()["data"]["members"][0]["user_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_id"])
        self.assertEqual(device_id2, res.json()["data"]["members"][0]["device_name"])
        self.assertEqual(app_id, res.json()["data"]["members"][0]["app_id"])
        self.assertEqual(1, len(res.json()["data"]["members"]))

        info_log("等待4s")
        time.sleep(4)

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

    def testCase15_location_check(self):
        """上报接口(v1/group/report/list):设备超出距离"""
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
            "location": {"latitude": 13.23232, "longitude": 123.433},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 30000
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

    def testCase16_group_type_1(self):
        """上报接口(v1/group/report/list):group_type [1]"""
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
            "expire": 30000
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
            "group_type": [1],
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

        info_log("用户2上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 13.23232, "longitude": 123.433},
            "network": {"lan": "127.0.0.1/24"},
            "expire": 30000
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
            "group_type": [1],
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

    @unittest.skip("出口ip暂无法校验")
    def testCase17_group_type_2(self):
        """上报接口(v1/group/report/list):group_type [2]"""
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
            "expire": 30000
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
            "group_type": [2],
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

        info_log("用户2上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.0.2/24"},
            "expire": 30000
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
            "group_type": [2],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(res.json()["data"]["members"]))

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

    def testCase18_group_type_3(self):
        """上报接口(v1/group/report/list):group_type [3]"""
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
            "network": {"lan": "127.0.0.23/24"},
            "expire": 30000
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
            "group_type": [3],
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

        info_log("用户2上报消息")
        body = {
            "identify_info": {
                "app_id": app_id,
                "user_id": str(self.userId2),
                "device_id": device_id2
            },
            "location": {"latitude": 13.23232, "longitude": 123.333},
            "network": {"lan": "127.0.1.2/24"},
            "expire": 30000
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
            "group_type": [3],
            "location": {"location_radius": 10}
        }
        res = self.v1gr.post_v1_group_report_list(self.host, body, self.sid1, self.ak, self.sk)
        info_log("response: {}".format(res.json()))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(res.json()["data"]["members"]))

        info_log("删除设备信息")
        res = self.v1d.delete_v1_device(self.host, self.sid1, device_id, app_id, self.userId1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])

        res = self.v1d.delete_v1_device(self.host, self.sid2, device_id2, app_id, self.userId2)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()["code"])
