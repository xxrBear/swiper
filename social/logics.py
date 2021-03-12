import datetime

from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friends
from libs.cache import rds
from common import keys
from swiper import config
from common import stat


def rcmd_from_db(uid, num):
    """机器人用户"""
    profile, _ = Profile.objects.get_or_create(id=uid)

    today = datetime.date.today()
    # 最早出生的人生日
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚出生的人的生日
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 排除滑动过的人
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    ).exclude(id__in=sid_list)[:num]
    return users


def users_from_rds(uid):
    """从Redis中提取用户"""
    user_id_list = rds.lrange(keys.FIRST_RCMD_K % uid, 0, 19)
    users = [user for user in User.objects.filter(id__in=user_id_list)]
    return users


def rcmd(uid):
    """数据库与Redis用户和"""
    rds_users = users_from_rds(uid)
    count = 20 - len(rds_users)
    db_users = rcmd_from_db(uid, count)
    users = list(rds_users) + list(db_users)
    return users


def like_someone(uid, sid):
    """
    喜欢某人函数
    1.Swiped表中记录喜欢某人
    2.检查Swiped表中对方是否喜欢过我
    3.如果喜欢匹配成好友
    :param uid:
    :param sid:
    :return: True or False or None
    """
    Swiped.swipe(uid, sid, stype='like')

    # 删除滑动过的推荐
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    if Swiped.is_liked(sid, uid):
        Friends.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    Swiped.swipe(uid, sid, stype='superlike')

    # 删除滑动过的推荐
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    liked_me = Swiped.is_liked(sid, uid)

    if liked_me:
        Friends.make_friends(uid, sid)
        return True
    elif liked_me == False:
        return False
    else:
        # 对方并没有滑动过uid,将uid添加到对方的“优先推荐队列”
        rds.rpush(keys.FIRST_RCMD_K % sid, uid)
        return False


def dislike_someone(uid, sid):
    Swiped.swipe(uid, sid, stype='dislike')
    # 删除滑动过的推荐
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)


def rewind_swiper(uid):
    """
    反悔最近5分钟的操作
    每天只能反悔3次
    """
    # 取出当前时间
    now = datetime.datetime.now()

    # 取出反悔key的过期时间，如果没有给一个默认值
    rewind_key = keys.REWIND_K % (now.date(), uid)
    rewind_times = rds.get(rewind_key, 0)

    # 检查key的反悔次数，如果超过3次则抛出错误
    if rewind_times > 3:
        raise stat.REWIND_TIMEOUT_ERR

    # 从数据库中取出最近滑动记录
    latest_swipe = Swiped.objects.filter(uid=uid).latest('stime')

    # 5分钟内可以撤销滑动，过时则抛错
    pass_time = now - latest_swipe.stime
    if pass_time.total_seconds() > config.TIMEOUT:
        raise stat.REWIND_TIME_ERR

    # 如果是超级喜欢，那么要把自己从对方的优先推荐队列中删去,好友表记录删去
    if latest_swipe.stype == 'superlike':
        rds.lrem(keys.FIRST_RCMD_K % latest_swipe.sid, 1, uid)
        Friends.break_off(latest_swipe.sid, uid)

    # 如果是超级喜欢和喜欢类型，那么要把好友表记录删去
    elif latest_swipe.stype == 'like':
        Friends.break_off(latest_swipe.sid, uid)

    # 删除滑动记录
    latest_swipe.delete()

    # 更新反悔次数
    rds.set(rewind_key, rewind_times + 1, 86400)


def users_like_me(uid):
    """
    查看谁喜欢我函数
    """
    # 我滑动过的人的id
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 喜欢或者超级喜欢我的人id
    like_types = ['like', 'superlike']
    uid_list = Swiped.objects.filter(sid=uid, stype__in=like_types) \
        .exclude(uid__in=sid_list).values_list('uid', flat=True)

    users = User.objects.filter(id__in=uid_list)

    return users


def my_friends(uid):
    friends = Friends.friends_list(uid=uid)
    users = User.objects.filter(id__in=friends)
    return users
