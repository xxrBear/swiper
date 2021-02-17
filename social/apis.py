from libs.http import render_json
from swiper import logics


def rcmd_user(request):
    """推荐用户接口"""
    users = logics.rcmd(request.uid)
    user_data = [user.to_dict() for user in users]

    return render_json(data=user_data)
