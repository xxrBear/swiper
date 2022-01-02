# 返回码设置
OK = 0


class LogicErr(Exception):
    """逻辑异常类，作为一个总类，目的是为了容易被中间件捕获"""
    code = None  # 感觉没什么用
    data = None

    def __init__(self, data=None):
        self.data = data or self.__class__.__name__


def gen_logic_err(name, code):
    """直接返回逻辑异常类，不用写class来继承"""
    return type(name, (LogicErr,), {"code": code})


SEND_SMS_ERR = gen_logic_err('SEND_SMS_ERR', 1000)              # 发送短信错误
VCODE_ERR = gen_logic_err('VCODE_ERR', 1001)                    # 验证码输入错误
LOGIN_REQUIRED_ERR = gen_logic_err('LOGIN_REQUIRED_ERR', 1002)  # 登录错误
USER_FROM_ERR = gen_logic_err('USER_FROM_ERR', 1003)            # 用户资料验证错误
PROFILE_FORM_ERR = gen_logic_err('PROFILE_FORM_ERR', 1004)      # 社交资料验证错误
STYPE_ERR = gen_logic_err('STYPE_ERR', 1005)                    # 滑动类型错误
RESWIPE_ERR = gen_logic_err('RESWIPE_ERR', 1006)                # 重复滑动的错误
REWIND_TIME_ERR = gen_logic_err('REWIND_TIME_ERR', 1007)        # 滑动超时错误
REWIND_TIMEOUT_ERR = gen_logic_err('REWIND_TIMEOUT_ERR', 1008)  # 滑动次数上限错误
VipouttimeErr = gen_logic_err('VipouttimeErr', code=1009)       # 你的Vip权限超时了
RequirepermErr = gen_logic_err('RequirepermErr', code=1010)     # 你没有这个VIP权限
