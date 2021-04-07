# 云之讯平台设置
YZX_URL = "https://open.ucpaas.com/ol/sms/sendsms"

YZX_COF = {
    "sid": "0d1fcfbe6b82e2c8aee9fca3eec81230",
    "token": "eba5641d0019e558751f5f0b5e63d672",
    "appid": "cafa0e32d0e14a019e104625588263fa",
    "templateid": "541376",
    "param": None,
    "mobile": None,
}

# 阿里云配置
ALI_AK = '妈蛋,不给我用'
ALI_SK = 'dSS1yCCL3Qv15CkMx50q2f9RDFamgV'

ali_url = 'https://bearxxr.oss-cn-shanghai.aliyuncs.com/'

# Redis配置
REDIS = {
    'host': 'localhost',
    'db': 5,
    'port': 6379
}

# 反悔接口配置
TIMES = 3           # 反悔次数
TIMEOUT = 5 * 60    # 反悔时间5分钟

# 热度分数配置
HOT_RANK_SCORE = {
    'like': 5,
    'superlike': 7,
    'dislike': -5
}