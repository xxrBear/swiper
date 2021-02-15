from django.http import JsonResponse
from django.core.cache import cache

from user import logics
from common import stat
from user.forms import UserForm, ProfileForm
from user.models import User, Profile
from libs.http import render_json


def get_vcode(request):
    """得到验证码接口"""
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return render_json()
    else:
        return render_json(code=stat.SEND_SMS_ERR)


def sumbit_vcode(request):
    """提交验证码接口"""
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cache_vcode = cache.get("vcode-%s" % phonenum)
    if vcode and cache_vcode == vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum)

        request.session['uid'] = user.id

        return render_json(data=user.to_dict())
    else:
        return render_json(code=stat.VCODE_ERR)


def get_profile(request):  # 获取个人资料
    profile, _ = Profile.objects.get_or_create(id=request.uid)
    return JsonResponse(data=profile.to_dict())


def set_profile(request):
    """修改个人资料接口"""
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if not user_form.is_valid():
        return render_json(code=stat.USER_FROM_ERR, data=user_form.errors)
    if not profile_form.is_valid():
        return render_json(code=stat.PROFILE_FORM_ERR, data=profile_form.errors)

    # 保存数据
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)
    Profile.objects.filter(id=request.uid).update(**profile_form.cleaned_data)

    return render_json()
