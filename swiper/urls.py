"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from user import apis as user_api
from social import apis as social_api

urlpatterns = [
    # user模块
    url(r'^user/api/get_vcode', user_api.get_vcode),
    url(r'^user/api/sumbit_vcode', user_api.sumbit_vcode),
    url(r'^user/api/get_profile', user_api.get_profile),
    url(r'^user/api/set_profile', user_api.set_profile),
    url(r'^user/api/upload_avatar', user_api.upload_avatar),

    # social模块
    url(r'^social/api/rcmd_user$', social_api.rcmd_user),
    url(r'^social/api/like$', social_api.like),
]
