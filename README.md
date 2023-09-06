# swiper

##   swiper 是一个前后端分离的项目，目前有三个模块，User、Social、VIP

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

## Celery

详细可参考:
    
Celery官方文档
https://docs.celeryproject.org/en/latest/

Celery中文文档
https://www.celerycn.io/ 

Celery经典示例:

https://cloud.tencent.com/developer/article/1525682

https://mp.weixin.qq.com/s/lXrp3igYo9W2UuE5Gauysg

https://www.cnblogs.com/wdliu/p/9530219.html









