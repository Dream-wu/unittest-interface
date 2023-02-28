import requests
import json
from common.unittest_report_logs import info_log


class V1Device(object):

    # 设备能力注册
    @staticmethod
    def post_v1_device_register(host, params, sid):
        uri = "/api/v1/device/register"
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'cookie': 'wps_sid={}'.format(sid),
            # "Client-Env": "gray-test"
        }
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, data=json.dumps(params))

        return res

    # 删除设备信息
    @staticmethod
    def delete_v1_device(host, sid, device_id, app_id, user_id):
        uri = "/api/v1/device/{}/apps/{}/users/{}".format(device_id, app_id, user_id)
        url = host + uri
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Content-Type': 'application/json',
            'cookie': 'wps_sid={}'.format(sid),
            # "Client-Env": "gray-test"
        }
        info_log("url: {}".format(url))
        res = requests.delete(url=url, headers=headers)

        return res
