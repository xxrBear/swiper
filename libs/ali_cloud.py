# -*- coding: utf-8 -*-

import os

import oss2

from swiper import config


def upload_to_ali(filename, filepath):
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', config.ALI_AK)
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', config.ALI_SK)
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'bearxxr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')

    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    # 先输入本地文件名，再设置oss上的名字
    bucket.put_object_from_file(filepath, filename)

    return
