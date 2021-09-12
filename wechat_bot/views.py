#wechat chatbot
import logging
import redis
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponse

from werobot import WeRoBot
from werobot.session.redisstorage import RedisStorage
from obrx.settings.base import env
from utils.wx_config import get_access_token
from users.models import User
from wechat_bot.processing import handle_wechat_user, upload_classifieds


url = urlparse(settings.REDIS_URL)
db = redis.Redis(host=url.hostname, port=6379)
session_storage = RedisStorage(db, prefix="wxbot_")
wxbot = WeRoBot(
            token=env('WXBOT_TOKEN'),
            app_id=env('WECHAT_APPID'),
            app_secret=env('WECHAT_APPSECRET'),
            enable_session=True,
            session_storage=session_storage
        )

#client=wxbot.client


@wxbot.handler
def hello(message):
    return 'Hello World!'


@wxbot.text
def handle_text(message, session):
    userid = message.source
    handle_wechat_user(userid)
    return ''


@wxbot.image
def handle_img(message, session):
    img = message.img
    handle_wechat_user(userid)

    user = User.objects.filter(
            wechat_openid=userid
        )
    if user.count() > 0:
        upload_classifieds(message, user.first())
    return ''


@wxbot.subscribe
def handle_subscribe(message):
    return "Thanks for following us. Send photos of your stuff for sale here & we'll upload for you😊" #noqa


@wxbot.pic_photo_or_album
def handle_photo_or_album(message):
    userid = message.source
    handle_wechat_user(userid)

    user = User.objects.filter(
            wechat_openid=userid
        )
    if user.count() > 0:
        upload_classifieds(message, user.first())
    return ''


def set_custom_menu(request):
    token = get_access_token()
    if token is None:
        return HttpResponse(
            "Hey, token cannot be accessed",
            content_type='text/plain'
        )

    try:
        response = requests.get(
            url=f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={token}", #noqa
            params={
                "button": [
                    {
                        "type": "view",
                        "name": "Items",
                        "url": "https://obrisk.com/classifieds/"
                    },
                    {
                        "type": "pic_photo_or_album",
                        "name": "Post New",
                        "key": "rselfmenu_1_1",
                        "sub_button": [ ]
                    }
                ]

            }
        )
        response.encoding = 'utf8'
        return HttpResponse(
            f"Results, {string(response)}",
            content_type='text/plain'
        )

    except (AttributeError,
            TypeError,
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:

        return HttpResponse(
            f"Failed, {e}",
            content_type='text/plain'
        )
    return None
