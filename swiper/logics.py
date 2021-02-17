import datetime

from user.models import User, Profile


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
    )

    return users
