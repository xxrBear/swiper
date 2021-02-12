import random
import copy

import requests
from django.core.cache import cache

from swiper import config


def get_random_vcode(length=6):
    # 获取6位验证码
    return "".join([str(random.randint(0, 9)) for i in range(length)])


def send_vcode(phonenum):
    vcode = get_random_vcode()
    print(vcode)
    data = copy.copy(config.YZX_COF)

    data['param'] = vcode
    data['mobile'] = phonenum

    requests.post(url=config.YZX_URL, data=data)

    # 假的，因为云之讯有问题
    if requests.post(url=config.YZX_URL, data=data).status_code != 200:
        cache.set('vcode-%s' % phonenum, vcode, 18000)
        return True
    else:
        return False
