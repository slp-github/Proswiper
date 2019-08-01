import datetime

from django.core.cache import cache
from django.db import models

# Create your models here.
from libs.orm import ModelToDictMixin

SEXS = (
    (0, "未知"),
    (1, "男"),
    (2, "女"),
)

LOCATIONS = (
    ("gz", "广州"),
    ("sz", "深圳"),
    ("sh", "上海"),
    ("cd", "成都"),
    ("bj", "北京"),
    ("cq", "重庆"),
    ("hz", "杭州"),

)

class User(models.Model):

    phonenum = models.CharField(max_length=16,unique=True)
    nickname = models.CharField(max_length=18,)
    sex = models.IntegerField(choices=SEXS,default=0)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location  = models.CharField(max_length=16,choices=LOCATIONS,default="gz")

    @property #将方法变成属性
    def age(self):
        today = datetime.date.today()
        dd=today.day-self.birth_day
        dm = today.month-self.birth_month
        dy = today.year-self.birth_year
        if dd < 0:
            dd = dd + 30
            dm = dm - 1
            # checks if difference in month is negative when difference in day is also negative
            if dm < 0:
                dm = dm + 12
                dy = dy - 1
        # checks if difference in month is negative when difference in day is positive
        if dm < 0:
            dm = dm + 12
            dy = dy - 1
        return dy
    @property
    def profile(self):
        if not hasattr(self,'_profile'):
            self._profile,_ = Profile.objects.get_or_create(pk=self.id) #以User表的id作为Profile表的id ，以此建立关联
        return self._profile
    def to_dict(self):
        return {
            'uid':self.id,
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'sex':self.sex,
            'avatar':self.avatar,
            'location':self.location,
            'age':self.age
        }

    # def get_or_create_token(self):
    #     '''
    #     为用户生成一个唯一token
    #     :return:
    #     '''
    #     key = 'token:{}'.format(self.id)
    #     token = cache.get(key)
    #     if not token:
    #         token ='token.......23saeq5452145HAGD'
    #         cache.set(key,token,24*60*60)
    #         cache.set(token,uid,24*60*60)
    #     return token

    class Meta:
        db_table = 'users'


class Profile(models.Model,ModelToDictMixin):#通过Mixin拓展子类的功能。ModelToDictMixin功能相当于to_dict
    """
    location        目标城市
    min_distance    最小查找范围
    max_distance    最大查找范围
    min_dating_age  最小交友年龄
    max_dating_age  最大交友年龄
    dating_sex      匹配的性别

    auto_play       视频自动播放

    user.profile.location
    """
    location = models.CharField(max_length=16,choices=LOCATIONS,default='gz')
    min_distance = models.IntegerField(default=0)
    max_distance = models.IntegerField(default=10)
    min_dating_age = models.IntegerField(default=18)
    max_dating_age = models.IntegerField(default=30)
    dating_sex = models.IntegerField(choices=SEXS,default=0)

    auto_play = models.BooleanField(default=True)

    class Meta:
        db_table = 'profiles'