import random
import re


'''
正则验证手机号格式
'''
PHONE_PATTERN  = re.compile(r'^1[3-9]\d{9}$')

def is_phone_num(phone_num):
    print(phone_num)

    return True if PHONE_PATTERN.match(phone_num.strip()) else False #phone_num.strip()手机号前后去空格


def gen_random_code(length=4):
    if not isinstance(length,int):#判断length是否是数字
        length=4

    if length <=0:
        length=4
    code = random.randrange(10**(length-1),10**(length))
    return str(code)