from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from common import errors
from common.errors import LogicException, LogicError
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        '''
        通过session自定义认证中间件

        白名单
        request.path
         根据request.session['uid']判断登录状态
        :param request:
        :return:
        '''
        WHITE_LIST = [
            '/api/user/verify-phone',
            '/api/user/login'
        ]

        if request.path in WHITE_LIST:
            return
        uid = request.session.get('uid')

        print('uid',uid)
        if not uid:
            return render_json(code=errors.LOGIN_REQUEST_ERR)

        request.user = User.objects.get(pk=uid)

        # token = request.META.get('HTTP_X_SWIPER_AUTH_TOKEN')
        #
        # uid  = cache.get(token)
        # if not token:
        #     return render_json(code=errors.LOGIN_REQUEST_ERR)
        # request.user = User.objects.get(pk = uid)#通过模型获取uid,然后赋值给user


class LogicExcepttionMiddleware(MiddlewareMixin):

    def process_exception(self,request,exception):
        if isinstance(exception,(LogicException,LogicError)):
            return render_json(code= exception.code)

