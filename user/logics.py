import random
import copy

import requests
from django.http import JsonResponse

from swiper import config


def get_random_vcode(length=6):
    # 获取6位验证码
    return "".join([str(random.randint(0, 9)) for i in range(length)])


def sumbit_vcode(phonenum):
    vcode = get_random_vcode()
    print(vcode)
    data = copy.copy(config.YZX_COF)

    data['param'] = vcode
    data['mobile'] = phonenum

    requests.post(url=config.YZX_URL, data=data)
