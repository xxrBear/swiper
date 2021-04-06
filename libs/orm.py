from django.db import models
from django.db.models import query

from libs.cache import rds
from common.keys import MODEL_K


def get(self, *args, **kwargs):
    """自定义 get 方法处理缓存"""
    
    model_cls_name = self.model.__name__  # 模型的类名

    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        model_key = MODEL_K % (model_cls_name, pk)
        model_obj = rds.get(model_key)
        if isinstance(model_obj, self.model):
            return model_obj
    
    # 如果缓存里面找不到，再到数据库中查找,然后写入缓存
    model_obj = self._get(*args, **kwargs)
    model_key = MODEL_K % (model_cls_name, model_obj.pk)
    model_obj = rds.set(model_key, model_obj)

    return model_obj


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    '''自定义 save 处理缓存'''

    # 调用原方法将数据保存至数据库
    self._get(force_insert, force_update, using, update_fields)

    # 将数据保存至缓存中
    model_key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(model_key, self)


def patch_model():
    """通过 Monky Patch 的方式动态的为 Model 添加缓存处理"""
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save

