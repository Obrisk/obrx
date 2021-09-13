
from utils.wx_config import get_access_token, get_user_info
from users.tasks import upload_image
from users.models import User, WechatUser

def handle_wechat_user(userid):
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
            province_region=user_info['province'].encode('iso8859-1').decode('utf-8'),
            country=user_info['country'].encode('iso8859-1').decode('utf-8')
        )


def upload_img(message):
    pass
