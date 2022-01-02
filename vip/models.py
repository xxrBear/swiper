from django.db import models


class Vip(models.Model):
    '''会员表'''

    name = models.CharField(max_length=10, unique=True, verbose_name='会员的名字,是青铜还是白银')
    level = models.IntegerField(default=0, verbose_name='等级')
    price = models.FloatField(default=0.0, verbose_name='价格')
    days = models.IntegerField(default=0, verbose_name='时间')

    def has_permission(self, perm_name):
        '''
        检测当前用户是否有对应的权限
        '''
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()

    class Meta:
        db_table = 'vip'


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=20, verbose_name='权限的名称', unique=True)
    desc = models.TextField(verbose_name='权限描述')

    class Meta:
        db_table = 'permission'


class VipPermRelation(models.Model):
    '''会员与权限的对应关系表'''

    vip_id = models.IntegerField(verbose_name='会员ID')
    perm_id = models.IntegerField(verbose_name='权限ID')

    class Meta:
        db_table = 'vippermrelation'