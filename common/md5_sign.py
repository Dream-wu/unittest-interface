import requests
import hashlib
import base64
import json
import datetime
import hmac


class Md5Sign(object):
    def get_md5_content(self, body):
        get_md5_data = hashlib.md5()
        get_md5_data.update(str(body).encode("utf-8"))
        content_md5 = str(base64.b64encode(get_md5_data.digest()), "utf-8")
        return content_md5

    def new_signature(self, request_method, uri_path, access_key, secret_key,  client_type, content_type=None, content_md5=None):
        """
        签名算法
        """
        date = datetime.datetime.utcnow()
        date = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        sign_arr = []
        for v in [request_method, uri_path, date, content_md5, content_type, client_type]:
            if v is not None:
                sign_arr.append(v.lower())
        sign_str = '&'.join(sign_arr)

        aa = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'),digestmod=hashlib.sha1).hexdigest()
        signature = base64.b64encode(aa.encode('utf-8')).decode()
        return 'WPS:%s:%s' % (access_key, signature), date
