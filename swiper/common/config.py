'''
业务相关配置
'''

#云之讯短信平台配置

YZX_SMS_URL = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_SMS_PARAMS = {"sid": "d0aab60f9ba4312de1376b71c111c38e",
    "token": "a7d82f91d50aaa707ffcf30016093900",
    "appid": "da9ecc3d0c5d4ccea12d98f544f8b69f",
    "templateid": "486149",
    "param": "",
    "mobile": "",
    "uid": "2d92c6132139467b989d087c84a365d8"}


#七牛云存储配置
QN_ACCESS_KEY = 'p7gEO8AsOwxdz9SRvs8uxcKZqnadV8er3qPBK8Rp'
QN_SECRET_KEY = 'fl448xAE0lndq-usCTojwSkiLt5yqFcFJRa_xA26'
QN_BUCKET_NAME = 'swiper'
QN_HOST = 'pvhvy246n.bkt.clouddn.com'

#每日反悔次数设置
SWIPE_LIMIT = 3