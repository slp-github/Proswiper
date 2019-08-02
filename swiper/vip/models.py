from django.db import models

# Create your models here.
from libs.orm import ModelToDictMixin


class Vip(models.Model,ModelToDictMixin):
    '''
    会员表

    '''
    level = models.IntegerField(default=0,unique=True)
    name =  models.CharField(max_length=128,unique=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,default=0)#带精度的浮点型，总共五位数，小数点后面两位
    @property
    def perms(self):
        '''
        当前vip所对应的权限
        :return:
        '''
        if not hasattr(self,'_perms'):
            # 通过vip.id从vip-perission关系表中获得对应的perm.id
            vip_perms = VipPerission.objects.filter(vip_id=self.id).only('perm_id')
            #print('vip_perms',vip_perms)
            perms_id_list = [p.perm_id for p in vip_perms]

            # 通过perm_id 获得perm
            self._perms = Permission.objects.filter(id__in=perms_id_list)

        return self._perms

    def _has_perm(self,perm_name):
        '''
        检查当前vip是否拥有某种权限
        :param perm_name:
        :return:
        '''
        perm_names = [p.name for p in self.perms]
        #print('perm_names',perm_names)
        return perm_name in perm_names

    class Meta:
        db_table='vips'


class Permission(models.Model,ModelToDictMixin):
    '''
    权限表
    '''
    name = models.CharField(max_length=32,unique=True)
    description = models.CharField(max_length=512)

    class Meta:
        db_table = 'permissions'


class VipPerission(models.Model):
    '''
    会员、权限 关系表
    '''
    vip_id = models.IntegerField()
    perm_id =  models.IntegerField()

    class Meta:
        db_table='vipperissions'