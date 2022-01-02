from user.models import User
from common import stat


def require_permission(perm_name):
    def wrapper1(view_func):
        def wrapper2(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)

            if user.is_vip_expired():
                # 检测VIP超时
                raise stat.VipouttimeErr

            if user.vip.has_permission(perm_name):
                # 检测用户是否有这个权限
                response = view_func(request, *args, **kwargs)
                return response
            else:
                raise stat.RequirepermErr

        return wrapper2

    return wrapper1
