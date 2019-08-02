'''
业务状态码、错误码
'''

OK = 0

#系统保留状态码
#1000-1999


#用户系统
#2000-2999
PHONE_NUM_ERR = 2001   #手机号格式错误
SMS_SEND_ERR = 2002 #验证码发送失败
VERIFY_CODE_ERR = 2003 #验证码错误
LOGIN_REQUEST_ERR = 2004 #用户认证错误
AVATAR_UPLOAD_ERR = 2005 #头像上传失败

#社交系统
SID_ERR = 3001 #sid参数错误
SWIPER_ERR = 3002  #滑动动作错误
SWIPE_LIMIT_ERR =  3003


#两种抛出错误的方法


#方法一：定义一个类继承于Except

class LogicException(Exception):
    '''
    自定义逻辑异常类
    调用者通过参数，传递错误码

    '''
    def __init__(self,code):
        self.code = code


#方法二，使用type动态创建一个异常类
#创建一个基类
class LogicError(Exception):
    code=None

def gen_logic_error(name,code):
    return type(name,(LogicError,),{'code':code})


SidError = gen_logic_error('SidError',3001)
SwiperError = gen_logic_error('SwiperError',3002)
SwipeLimitError = gen_logic_error('SwipeLimitError',3003)#超过次数限制


#vip系统
VIPPermError = gen_logic_error('VIPPermError',4001) #vip权限错误