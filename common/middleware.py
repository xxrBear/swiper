from django.utils.deprecation import MiddlewareMixin

from common import stat
from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    path_while_list = [
        '/user/api/get_vcode',
        '/user/api/sumbit_vcode'
    ]

    def process_request(self, request):
        if request.path not in self.path_while_list:
            uid = request.session.get('uid')
            if not uid:
                return render_json(code=stat.LOGIN_REQUIRED)
            else:
                request.uid = uid
