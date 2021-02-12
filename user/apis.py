from django.http import JsonResponse
from django.core.cache import cache

from user import logics
from common import stat
from user.models import User


def get_vcode(request):
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def sumbit_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cache_vcode = cache.get("vcode-%s" % phonenum)
    print(cache_vcode)
    if vcode and cache_vcode == vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum)

        request.session['uid'] = user.id

        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})
