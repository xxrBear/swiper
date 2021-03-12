from django.db import models
from django.db.models import Q
from django.db.utils import IntegrityError

from common import stat


class Swiped(models.Model):
    """滑动记录表"""
    STYPE = (
        ('like', '滑动，喜欢'),
        ('superlike', '滑动，超级喜欢'),
        ('dislike', '滑动 不喜欢')
    )
    uid = models.IntegerField(verbose_name='用户自己')
    sid = models.IntegerField(verbose_name='用户滑动过的人')
    stype = models.CharField(verbose_name='滑动的类型', max_length=16, choices=STYPE)
    stime = models.DateTimeField(verbose_name='添加日期', auto_now_add=True)

    @classmethod
    def swipe(cls, uid, sid, stype):
        """添加滑动记录方法"""
        if stype not in ['like', 'superlike', 'dislike']:
            raise stat.STYPE_ERR
        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise stat.RESWIPE_ERR

    @classmethod
    def is_liked(cls, uid, sid):
        """判断用户是否喜欢过对方的类方法"""
        like_type = ['like', 'superlike']
        try:
            has_swiped = cls.objects.get(uid=uid, sid=sid)
            return has_swiped.stype in like_type
        except cls.DoesNotExist:
            return None

    class Meta:
        db_table = 'swiped'
        unique_together = [['uid', 'sid']]


class Friends(models.Model):
    """好友表"""
    uid1 = models.IntegerField(verbose_name='用户id')
    uid2 = models.IntegerField(verbose_name='用户id')

    @classmethod
    def make_friends(cls, uid1, uid2):
        """类方法：添加两个人的好友关系"""
        # 三元表达式把小的值放在前面
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def break_off(cls, uid1, uid2):
        """解除好友关系"""
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friends_list(cls, uid):
        """查看好友"""
        condition = Q(uid1=uid) | Q(uid2=uid)
        fid_list = []
        for fid in cls.objects.filter(condition):
            friend_id = fid.uid2 if fid.uid1 == uid else fid.uid1
            fid_list.append(friend_id)
        return fid_list

    class Meta:
        db_table = 'friends'
        unique_together = [['uid1', 'uid2']]
