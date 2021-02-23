from django.utils.deprecation import MiddlewareMixin

from common import stat
from common.stat import LogicErr
from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    """用户登录验证中间件"""
    path_while_list = [
        '/user/api/get_vcode',
        '/user/api/sumbit_vcode'
    ]

    def process_request(self, request):
        if request.path not in self.path_while_list:
            uid = request.session.get('uid')
            if not uid:
                return render_json(code=stat.LOGIN_REQUIRED_ERR)
            else:
                request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    """用户逻辑错误中间件"""

    def process_exception(self, request, exception):
        if isinstance(exception, LogicErr):
            return render_json(code=exception.code, data=exception.data)
