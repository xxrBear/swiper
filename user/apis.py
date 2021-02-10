from django.http import JsonResponse

from user import logics
from common import stat


def gend_vcode(request):
    phonenum = request.GET.get('phonenum')
    status = logics.sumbit_vcode(phonenum)
    if status:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})
