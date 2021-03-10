from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from redis import Redis as _Redis

from swiper.config import REDIS


class Redis(_Redis):
    """
    封装redis的get,set方法
    让get可以有默认值
    让set可以设置 列表类型[]
    """

    def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        pickle_value = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, pickle_value, ex, px, nx, xx, keepttl)

    def get(self, name, default=None):
        pickle_value = super().get(name)
        if not pickle_value:
            return default
        try:
            return loads(pickle_value)
        except UnpicklingError:
            return pickle_value


rds = Redis(**REDIS)
