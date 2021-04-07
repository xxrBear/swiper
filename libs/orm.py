import datetime

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
    rds.set(model_key, model_obj)

    return model_obj


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    """自定义 save 处理缓存"""

    # 调用原方法将数据保存至数据库
    self._save(force_insert, force_update, using, update_fields)

    # 将数据保存至缓存中
    model_key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(model_key, self)


def to_dict(self, *exclude_args):
    """为 model 添加统一的 to_dict 方法"""

    attr_dict = {}
    not_safe_attr = (datetime.date, datetime.datetime)

    for field in self._meta.fields:
        name = field.attname
        if name not in exclude_args:
            value = getattr(self, name)
            attr_dict[name] = str(value) if isinstance(self, not_safe_attr) else value

    return attr_dict


def patch_model():
    """通过 Monky Patch 的方式动态的为 Model 添加缓存处理"""
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save
    models.Model.to_dict = to_dict
