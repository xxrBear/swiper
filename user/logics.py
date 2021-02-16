import os
import random
import copy

import requests
from django.core.cache import cache

from swiper import config
from tasks import celery_app
from user.models import User
from libs.ali_cloud import upload_to_ali


def get_random_vcode(length=6):
    # 获取6位验证码
    return "".join([str(random.randint(0, 9)) for i in range(length)])


def send_vcode(phonenum):
    # 利用云之讯发短信
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


def save_avatar(uid, avatar):
    """本地保存头像函数"""

    filename = 'avatar-%s' % uid
    filepath = '/tmp/%s' % filename

    with open(filepath, 'wb') as f:
        for chunk in avatar.chunks():
            f.write(chunk)

    return filename, filepath


@celery_app.task
def upload_avatar(uid, avatar_file):
    """头像上传至阿里云"""

    filename, filepath = save_avatar(uid, avatar_file)  # 保存至本地
    url = upload_to_ali(filename, filepath)  # 上传至阿里云oss
    User.objects.filter(id=uid).update(avatar=url)  # 修改数据库内容

    os.remove(filepath)  # 删除本地文件
