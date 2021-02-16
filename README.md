# swiper

##   swiper 是一个前后端分离的项目，目前是测试哦！目前有三个模块，User、Swiper、VIP

###  User模块

####  接口:

```
127.0.0.1:8000/user/api/get_vcode     # 发送手机验证码
127.0.0.1:8000/user/api/sumbit_vcode  # 提交手机验证码
127.0.0.1:8000/user/api/get_profile   # 获取个人资料
127.0.0.1:8000/user/api/set_profile   # 修改个人资料
127.0.0.1:8000/user/api/upload_avatar # 上传头像
```
## Celery配置
**重试:Retrying**

例子:

    @app.task(bind=True)
    def send_mail(self):
        '''发送email逻辑'''
        try:
            假装有代码
        except Exception as e:
            raise self.retry(exc=e, countdown=3, max_retries=3)
    
    retry的参数可以有: 
            exc: 指定抛出的异常
            throw: 重试时是否通知worker是重试任务
            eta: 指定重试的时间／日期
            countdown: 每多少秒重试一次
            max_retries: 最大重试次数
上述案例用shared_task装饰器也可以使用。

详细可参考:
    
Celery官方文档
https://docs.celeryproject.org/en/latest/

Celery中文文档
https://www.celerycn.io/ 

Celery经典示例

https://cloud.tencent.com/developer/article/1525682

https://mp.weixin.qq.com/s/lXrp3igYo9W2UuE5Gauysg

https://www.cnblogs.com/wdliu/p/9530219.html









