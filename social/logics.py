import datetime

from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friends


def rcmd(uid):
    """机器人用户"""
    profile, _ = Profile.objects.get_or_create(id=uid)

    today = datetime.date.today()
    # 最早出生的人生日
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚出生的人的生日
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    )[:20]

    return users


def like_someone(uid, sid):
    """
    喜欢某人函数
    1.Swiped表中记录喜欢某人
    2.检查Swiped表中对方是否喜欢过我
    3.如果喜欢匹配成好友
    :param uid:
    :param sid:
    :return: True or False
    """
    Swiped.objects.create(uid=uid, sid=sid, stype='like')
    if Swiped.is_liked(sid, uid):
        Friends.make_friends(uid, sid)

        return True
    else:
        return False
