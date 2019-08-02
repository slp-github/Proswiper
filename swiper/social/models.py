from django.db import models

# Create your models here.
from django.db.models import Q

from common import errors
from common.errors import LogicException
from social.managers import FriendManger


class Swiped(models.Model):
    '''
    滑动记录
    '''
    MARKS = (
        ('like','喜欢'),
        ('dislike','不喜欢'),
        ('superlike','超喜欢'),
    )
    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16,choices=MARKS)
    creat_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def swipe(cls,uid,sid,mark):
        '''
        创建滑动记录，如果存在记录，则返回False,否则返回True
        :param uid:
        :param sid:
        :param mark:
        :return:
        '''
        marks=[m for m,_ in cls.MARKS]
        if mark not in marks:
            #raise LogicException(errors.SWIPER_ERR)#第一种抛出错误的方式
            raise errors.SwiperError  #第二种抛出错误的方法
        if cls.objects.filter(uid=uid,sid=sid).exists():
            return False
        else:
            cls.objects.create(uid=uid,sid=sid,mark=mark)
            return True

    @classmethod
    def is_liked(cls,uid,sid):
        return cls.objects.filter(uid=uid,sid=sid,mark__in=['like','superlike']).exists()

    class Meta:
        db_table = 'swiped'


class Friend(models.Model):
    '''
    好友关系
    '''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    objects = FriendManger()

    @classmethod
    def make_friends(cls,uid1,uid2):
        '''
        建立好友关系

        通过自定义，uid排序规则，来组织好友关系，且一组好友关系只保存一份数据
        :param uid1:
        :param uid2:
        :return:
        '''
        uid1,uid2 =  (uid1,uid2) if uid1>uid2 else (uid2,uid1)
        return cls.objects.get_or_create(uid1=uid1,uid2=uid2)
    @classmethod
    def cancel_friend(cls,uid1,uid2):
        uid1, uid2 = (uid1, uid2) if uid1 > uid2 else (uid2, uid1)
        cls.objects.filter(uid1=uid1,uid2=uid2).delete()

    @classmethod
    def friend_list(cls,uid):
        fid_list  = []
        friends = cls.objects.filter(Q(uid1=uid)|Q(uid2=uid))
        for f in friends:
            fid = f.uid1 if uid==f.uid2 else f.uid2
            fid_list.append(fid)
        return fid_list

    class Meta:
        db_table = 'friends'

