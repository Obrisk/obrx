#wechat chatbot
import logging
import redis
from django.conf import settings
from django.http import HttpResponse
from werobot import WeRoBot

from werobot.session.redisstorage import RedisStorage
from obrx.settings.base import env
from users.models import User, WechatUser
from utils.wx_config import get_access_token, get_user_info
from users.tasks import upload_image


#db = redis.Redis(settings.REDIS_URL)
#correct way is:
#db = redis.Redis(host=env('REDIS_HOST'), port=6379)
#session_storage = RedisStorage(db, prefix="wxbot_")
wxbot = WeRoBot(
            token=env('WXBOT_TOKEN'),
            app_id=env('WECHAT_APPID'),
            app_secret=env('WECHAT_APPSECRET'),
            enable_session=True
            #session_storage=session_storage
        )
client=wxbot.client


@wxbot.handler
def hello(message):
    return 'Hello World!'


@wxbot.text
def handle_text(message, session):
    userid = message.source
    logging.error(f'Obrx server: ID: {userid}')
    user = User.objects.filter(
            wechat_openid=userid
        )
    if user.count() == 0:
        wechat_user = WechatUser.objects.filter(
                wechat_openid=userid
            )
        if wechat_user.count() == 0:

            token = get_access_token()
            if token is None:
                logging.error('Wxbot failed to get access token')
                return ''

            user_info = get_user_info(token, userid)
            if user_info is None:
                logging.error('Wxbot failed to get user info')
                return ''

            picture = user_info['headimgurl']
            thumbnail = picture[:-3] + '64'
            full_image = picture[:-3] + '0'

            th, mid, full = upload_image(
               user_info['nickname'], thumbnail, picture, full_image
            )

            WechatUser.objects.create(
                name=user_info['nickname'],
                wechat_openid=user_info['openid'],
                thumbnail = th,
                picture = mid,
                org_picture = full,
                gender=user_info['sex'],
                city=user_info['city'].encode('iso8859-1').decode('utf-8'),
                province=user_info['province'].encode('iso8859-1').decode('utf-8'),
                country=user_info['country'].encode('iso8859-1').decode('utf-8')
            )

    return ''


@wxbot.image
def handle_img(message, session):
    img = message.img
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
            url=f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={token}",
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
