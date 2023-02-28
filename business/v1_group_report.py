import requests
import json
from copy import deepcopy
from common.md5_sign import Md5Sign
from common.unittest_report_logs import info_log


class V1GroupReport(object):

    # 设备信息上报接口
    @staticmethod
    def post_v1_group_report(host, params, sid, access_key, secret_key):
        uri = "/api/v1/group/report"
        url = host + uri
        content_type = "application/json"
        method = "post"
        client_type = "wps-android"
        content_md5 = Md5Sign().get_md5_content(str(params))
        authorization, date = Md5Sign().new_signature(request_method=method, content_type=content_type, uri_path=uri, access_key=access_key, secret_key=secret_key, client_type=client_type)
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Date': date,
            'Content-Type': 'application/json',
            "Client-Type": "wps-android",
            "Content_md5": content_md5,
            'Authorization': authorization,
            'cookie': 'wps_sid={}'.format(sid),
            # "Client-Env": "gray-test"
        }
        if sid == "pop":
            headers.pop("cookie")
        info_log("url: {}".format(url))
        info_log("request body: {}".format(json.dumps(headers)))
        res = requests.post(url=url, headers=headers, data=json.dumps(params))

        return res

    # 查询附近的设备成员信息
    @staticmethod
    def post_v1_group_report_list(host, params, sid, access_key, secret_key):
        uri = "/api/v1/group/report/list"
        url = host + uri
        content_type = "application/json"
        method = "post"
        client_type = "wps-android"
        content_md5 = Md5Sign().get_md5_content(str(params))
        authorization, date = Md5Sign().new_signature(request_method=method, content_type=content_type, uri_path=uri, access_key=access_key, secret_key=secret_key, client_type=client_type)
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Date': date,
            'Content-Type': 'application/json',
            "Client-Type": "wps-android",
            "Content_md5": content_md5,
            'Authorization': authorization,
            'cookie': 'wps_sid={}'.format(sid),
            # "Client-Env": "gray-test"
        }
        if sid == "pop":
            headers.pop("cookie")
        info_log("url: {}".format(url))
        res = requests.post(url=url, headers=headers, data=json.dumps(params))

        return res

    # 退出上报接口
    @staticmethod
    def delete_v1_group_report(host, params, sid, access_key, secret_key):
        uri = "/api/v1/group/report"
        url = host + uri
        content_type = "application/json"
        method = "delete"
        client_type = "wps-android"
        content_md5 = Md5Sign().get_md5_content(str(params))
        authorization, date = Md5Sign().new_signature(request_method=method, content_type=content_type, uri_path=uri, access_key=access_key, secret_key=secret_key, client_type=client_type)
        headers = {
            "Client-ver": "abc",
            "Client-type": "wps-android",
            'Date': date,
            'Content-Type': 'application/json',
            "Client-Type": "wps-android",
            "Content_md5": content_md5,
            'Authorization': authorization,
            'cookie': 'wps_sid={}'.format(sid),
            # "Client-Env": "gray-test"
        }
        if sid == "pop":
            headers.pop("cookie")
        info_log("url: {}".format(url))
        res = requests.delete(url=url, headers=headers, data=json.dumps(params))

        return res
