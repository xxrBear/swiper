from django.db import models


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ("北京", "北京"),
        ("上海", "上海"),
        ("深圳", "深圳"),
        ("郑州", "郑州"),
        ("西安", "西安"),
        ("成都", "成都"),
        ("沈阳", "沈阳"),
    )
    phonenum = models.CharField(verbose_name='手机', max_length=64, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='匿名用户')
    gender = models.CharField(verbose_name='性别', max_length=6, choices=SEX)
    birthday = models.DateField(verbose_name='生日', max_length=32, default='1990-01-01')
    location = models.CharField(verbose_name='常住地', max_length=256, choices=LOCATION)
    avatar = models.CharField(verbose_name='形象', max_length=256)

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'location': self.location,
            'avatar': self.avatar
        }

    class Meta:
        db_table = 'user'
