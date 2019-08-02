import datetime

from django.core.cache import cache

from common import cache_key, errors, config
from social.models import Swiped, Friend
from user.models import User

#按照设置好的要求，推荐用户
def recommend_user(user):
    today = datetime.date.today()
    '''
    计算年龄
    '''
    #最大匹配出生年分
    max_year = today.year-user.profile.min_dating_age
    #最小匹配出生年分
    min_year = today.year-user.profile.max_dating_age
    #被滑过的用户
    swiper_users = Swiped.objects.filter(uid=user.id).only('sid')
    print(swiper_users.query)#打印出相应的sql语句
    swiper_sid_list = [s.id for s in swiper_users]


    rec_users=User.objects.filter(
        location=user.profile.location,
        sex = user.profile.dating_sex,
        birth_year__gte=min_year,
        birth_year__lte=max_year

    ).exclude(id__in = swiper_sid_list)

    print(rec_users.query)#打印出相应的sql语句
    return rec_users

def like_someone(uid,sid):
    '''
    喜欢操作
    :param uid:
    :param sid:
    :return:
    '''
    ret = Swiped.swipe(uid=uid,sid=sid,mark='like')
    print('ret',ret)
    #如果相互喜欢则加为好友
    #select * from Swiper where uid=sid and sid = uid mark='like' or 'superlike'
    if ret and Swiped.is_liked(sid,uid):
        _,created = Friend.make_friends(uid,sid)

        #发送 匹配成功的推送消息
        return created
    else:
        return False


def superlike_someone(uid, sid):
    '''
    超喜欢操作
    :param uid:
    :param sid:
    :return:
    '''
    ret = Swiped.swipe(uid=uid, sid=sid, mark='superlike')
    # 如果相互喜欢则加为好友
    # select * from Swiper where uid=sid and sid = uid mark='like' or 'superlike'
    if ret and Swiped.is_liked(sid, uid):
        #Friend.make_friends(uid, sid)
        _, created = Friend.make_friends(uid, sid)#使用自定义管理器

        # 发送 匹配成功的推送消息
        return created
    else:
        return False


def rewind(user):
    '''
    撤销上一次滑动记录

    撤销上一次创建的好友关系
    :param user:
    :return:
    '''
    key = cache_key.SWIPE_LIMIT_PREFIX.format(user.id)
    swipe_times = cache.get(key,0)

    if swipe_times >=config.SWIPE_LIMIT:
        raise errors.SwipeLimitError


    swipe = Swiped.objects.filter(uid=user.id).latest('creat_at')
    if swipe.mark in ['like','superlike']:
        Friend.cancel_friend(swipe.uid,swipe.sid)
    swipe.delete()#删除滑动记录

    now = datetime.datetime.now()
    timeout = 86400 - now.hour*3600 - now.minute*60-now.second #过期时间
    cache.set(key, swipe_times + 1,timeout =timeout)


def like_me(user):
    '''
    查看喜欢过我的人，过滤掉已经存在的好友
    :param user:
    :return:
    '''
    friend_list = Friend.friend_list(user.id)
    # print('friend_list',friend_list)
    swipe_list = Swiped.objects.filter(sid=user.id,mark__in=['like','superlike']).exclude(uid__in=friend_list).only('uid')

    like_me_uid_list = [s.uid for s in swipe_list]
    return like_me_uid_list