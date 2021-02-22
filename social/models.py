from django.db import models


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
    datetime = models.DateTimeField(verbose_name='添加日期', auto_now_add=True)

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

    class Meta:
        db_table = 'friends'
        unique_together = [['uid1', 'uid2']]
