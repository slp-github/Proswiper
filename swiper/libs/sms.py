import requests
from django.conf import settings

from common.config import YZX_SMS_URL,YZX_SMS_PARAMS


def send_verify_code(phone_num,code):
    # 开发模式中就不使用短信发送请求，等正式上线再开启
    if settings.DEBUG ==True:
        print('send verify code',phone_num,code)
        return True

    params = YZX_SMS_PARAMS.copy() #防止配置参数该更改
    params['mobile'] = phone_num.strip()
    params['param'] = code

    resp  = requests.post(YZX_SMS_URL,json=params)
    # print(resp.json())

    if resp.status_code==200:
        ret=resp.json()
        if ret.get('code')=="000000":
            return True
    return False



