import json

from django.http import HttpResponse

from swiper import settings


def render_json(code=0, data=None):
    """渲染json返回值"""
    result = {
        'code': code,
        'data': data
    }

    if settings.DEBUG:
        json_result = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_result = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    return HttpResponse(json_result)
