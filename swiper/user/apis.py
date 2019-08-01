import os
import time

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common import errors, cache_key
from common.utils import is_phone_num
from libs.http import render_json
from swiper import settings
from user import logics
from user.forms import ProfileForm
from user.models import User


def verify_phone(request):

    '''
    #1 验证手机格式
    #2 生成验证码
    #3 保存验证码
    #4 发送验证码
    '''
    phone_num = request.POST.get('phone_num')

    if is_phone_num(phone_num):
        #如果验证码格式通过验证
        #生成验证吗
        if logics.send_verify_code(phone_num):
            return  render_json()
        else:
            return  render_json(code=errors.SMS_SEND_ERR)
    else:
        return render_json(code=errors.PHONE_NUM_ERR)


def login(request):
    '''
    登录或注册接口
    如果手机号存在，则登录，不存在则注册

    #1.检测验证码是否正确
    #2.注册或登录
    :param request:
    :return:
    '''
    phone_num = request.POST.get('phone_num','')
    code = request.POST.get('code','')

    phone_num = phone_num.strip()
    code  = code.strip()

    cache_code = cache.get(cache_key.VERIFY_CODE_CACHE_PREFIX.format(phone_num.strip()))
    #print("缓存code",cache_code)
    if cache_code !=code:

        return render_json(code=errors.VERIFY_CODE_ERR)

    #注册或登录(手机号存在则登录，不存在则注册)

    # try:
    #     user = User.objects.get(phone_num)
    # except User.DoesNotExist:
    #     user = User.objects.create()

    user,create = User.objects.get_or_create(phonenum=phone_num)

    #设置登录状态
    #session认证方式
    request.session['uid']=user.id

    #token认证方式
    #为当前登录用户生成一个token，并且存储到缓存中，key为：token：user.id,value为:token
    # token = user.get_or_create_toke()
    # data ={
    #     'token':token
    # }
    # return  render_json(data=data)

    return render_json(data=user.to_dict())


def get_profile(request):
    user = request.user
    return render_json(data=user.profile.to_dict(exclude=['auto_play']))


def set_profile(request):
    user = request.user
    form = ProfileForm(data=request.POST,instance=user.profile)#data要验证的数据，instance要使用到的约束

    if form.is_valid():
        form.save()
        return render_json()
    else:
        return render_json(data=form.errors)


def upload_avatar(request):
    user  =request.user
    avatar = request.FILES.get('avatar')
    #file_name = 'avatar-{}'.format(int(time.time()))

    # 1.先将文件上传至本地服务器
    # file_path = os.path.join(settings.MEDIA_ROOT,file_name)
    # with open(file_path,'wb+') as destinayion:
    #     for chunk in avatar.chunks():
    #         destinayion.write(chunk)
    #file_path = logics.upload_avatar(file_name,avatar)

    #2.将文件上传至七牛云
    # ret = logics.upload_avatar(file_name,file_path)
    # if ret:
    #     return render_json()
    # else:
    #     return render_json(code=errors.AVATAR_UPLOAD_ERR)

    logics.async_upload_avatar.delay(user,avatar)
    return render_json()