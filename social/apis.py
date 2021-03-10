from libs.http import render_json
from social import logics


def rcmd_user(request):
    """推荐用户接口"""
    users = logics.rcmd(request.uid)
    user_data = [user.to_dict() for user in users]
    return render_json(data=user_data)


def like(request):
    """喜欢某人接口"""
    sid = int(request.POST.get('sid'))
    is_match = logics.like_someone(request.uid, sid)
    return render_json({'is_match': is_match})


def superlike(request):
    """超级喜欢某人接口"""
    sid = int(request.POST.get('sid'))
    is_match = logics.superlike_someone(request.uid, sid)
    return render_json({'is_match': is_match})


def dislike(request):
    """不喜欢某人接口"""
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


def rewind(request):
    """反悔接口"""
    logics.rewind_swiper(request.uid)
    return render_json()
