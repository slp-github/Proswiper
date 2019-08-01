import os
import time
from urllib.parse import urljoin

from django.core.cache import cache

from common import utils, cache_key, config
from libs import sms, qiniuyun
from swiper import settings
from worker import celery_app


def send_verify_code(phone_num):
    '''
    发送验证码逻辑
    :param phone: 手机号
    :return:
    '''

    #生成验证码
    code = utils.gen_random_code(6)
    #发送验证码
    ret = sms.send_verify_code(phone_num,code)

    if ret:
        cache.set(cache_key.VERIFY_CODE_CACHE_PREFIX.format(phone_num.strip()),code,60*3)

    return ret

def upload_avatar(file_name,avatar):
    '''
    用户上传文件至本地
    :param file_name:
    :param avatar:
    :return:
    '''
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path,'wb+') as destinayion:
        for chunk in avatar.chunks():
            destinayion.write(chunk)
    return file_path

def upload_qiniuyun(filename,file_path):
    '''
    本地文件上传至七牛云
    :param filename:
    :param file_path:
    :return:
    '''
    ret,info  = qiniuyun.upload(file_name=filename,file_path=file_path)
    print(ret)

    return  True if info.status_code ==200 else False

@celery_app.task
def async_upload_avatar(user,avatar):
    '''
    异步上传头像
    :param avatar:
    :return:
    '''
    file_name = 'avatar-{}'.format(int(time.time()))

    file_path = upload_avatar(file_name,avatar)
    ret = upload_qiniuyun(file_name,file_path)
    if ret:
        #user.avatar=config.QN_HOST+'/'+file_name
        user.avatar = urljoin(config.QN_HOST,file_name)
        user.save()