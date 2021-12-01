"""obrx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from werobot.contrib.django import make_view
from wechat_bot.views import wxbot, set_custom_menu

urlpatterns = [
    path('',
        TemplateView.as_view(template_name="home.html"),
        name="home"
    ),
    path('signup/',
        TemplateView.as_view(template_name="signup.html"),
        name="signup"
    ),
    path('login/',
        TemplateView.as_view(template_name="login.html"),
        name="login"
    ),
    path('admin/', admin.site.urls),
    path('biR07IOg1Xgy66Hpypet-sh903821adua01d3d8l/',
        make_view(wxbot), name="wechat_users"
    ),
    path('set-custom-menu/biR07IOg1Xgy66Hpypet-sh903821adua01d3d8l/',
        set_custom_menu, name="set_custom_menu"
    ),
    path('MP_verify_HTQQQmxtxv6VNTtN.txt/',
        TemplateView.as_view(
            template_name='MP_verify_HTQQQmxtxv6VNTtN.txt',
            content_type='text/plain'
        ),
        name="wechat_mp_verify"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
