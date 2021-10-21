import uuid
import json
import base64
import os
import datetime
import logging
import requests

from django.db import IntegrityError

import oss2
from slugify import slugify
from utils.wx_config import get_access_token, get_user_info
from users.tasks import upload_image
from users.models import User, WechatUser
from utils.images_upload import bucket, bucket_name
from classifieds.models import ClassifiedImages


def handle_wechat_user(userid):
    if WechatUser.objects.filter(
        wechat_openid=userid).count() > 0:
        return WechatUser.objects.get(wechat_openid=userid)

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

    try:
        user = WechatUser.objects.create(
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
        return user
    except IntegrityError:
        user = WechatUser.objects.get(wechat_openid=user_info['openid'])
        return user

    except Exception:
        return ''


def upload_img(img, username):
    img_url = requests.get(img, timeout=360)
    salt = uuid.uuid4().hex[:12]

    img_name = "media/images/classifieds/" + slugify(username) + "/wxmessage/full-pic/" + salt + ".jpeg" #noqa
    thumb_name = "media/images/classifieds/" + slugify(username) + "/wxmessage/thumbnails/" + salt + ".jpeg" #noqa
    img_mid_name = "media/images/classifieds/" + slugify(username) + "/wxmessage/mid-size/" + salt + ".jpeg" #noqa
    style = 'image/resize,m_fill,h_156,w_156'
    style_mid = 'image/resize,m_pad,h_400'
    #style_mid = 'image/resize,m_fill,h_400'

    try:
        bucket.put_object(img_name, img_url.content)
        img_obj = ClassifiedImages(image=img_name)

        process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
            oss2.compat.to_string(base64.urlsafe_b64encode(
                oss2.compat.to_bytes(thumb_name))),
            oss2.compat.to_string(
                base64.urlsafe_b64encode(
                    oss2.compat.to_bytes(bucket_name)
                )
            )
        )
        bucket.process_object(img_name, process)

        process = "{0}|sys/saveas,o_{1},b_{2}".format(style_mid,
            oss2.compat.to_string(base64.urlsafe_b64encode(
                oss2.compat.to_bytes(img_mid_name))),
            oss2.compat.to_string(
                base64.urlsafe_b64encode(
                    oss2.compat.to_bytes(bucket_name)
                    )
                )
            )
        bucket.process_object(img_name, process)

    except Exception as e:
        #If there is a problem with the thumbnail generation,
        #our code is wrong
        logging.error(e, exc_info=e)
        img_obj.image_thumb = img_name

    else:
        img_obj.image_thumb = thumb_name

    if img_mid_name:
        img_obj.image_mid_size = img_mid_name
    img_obj.save()
    return img_name
