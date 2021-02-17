# swiper

##   swiper 是一个前后端分离的项目，目前是测试哦！目前有三个模块，User、Social、VIP

##  快速启动

+ 安装依赖包

  ```
  pip install -r requirements
  ```

+ 配置MySQL数据库

  修改settings中的数据库配置为你自己的配置

+ 启动Django、Celery环境

  ```
  python manage.py runserver
  celery worker -A tasks --loglevel==info
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









