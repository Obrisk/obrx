from utils.wx_config import get_access_token, get_user_info
from users.tasks import upload_image
from users.models import User, WechatUser
from utils.images_upload import bucket, bucket_name
from classifieds.models import ClassifiedImages

def handle_wechat_user(userid):
    if WechatUser.objects.filter(
        wechat_openid=userid).count() > 0:
        return ''

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
    if message.type == 'image':
        url_list = message.url
    elif message.type == 'pic_photo_or_album_event':
        url_list = message.pic_list

    logging.error(url_list)
    for url in url_list:
        continue
    return ''

    d = str(datetime.datetime.now())

    img_obj = ClassifiedImages(classified=obj, image=str_result)
    thumb_name = "media/images/classifieds/" + username + "/" + title + "/" + d + "/thumbnails/" + str(index) + ".jpeg" #noqa
    img_mid_name = "media/images/classifieds/" + username + "/" + title + "/" + d + "/mid-size/" + str(index) + ".jpeg" #noqa
    style = 'image/resize,m_fill,h_156,w_156'
    style_mid = 'image/resize,m_pad,h_400'
    #style_mid = 'image/resize,m_fill,h_400'

    try:
        process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
            oss2.compat.to_string(base64.urlsafe_b64encode(
                oss2.compat.to_bytes(thumb_name))),
            oss2.compat.to_string(
                base64.urlsafe_b64encode(
                    oss2.compat.to_bytes(bucket_name)
                )
            )
        )
        bucket.process_object(str_result, process)

        process = "{0}|sys/saveas,o_{1},b_{2}".format(style_mid,
            oss2.compat.to_string(base64.urlsafe_b64encode(
                oss2.compat.to_bytes(img_mid_name))),
            oss2.compat.to_string(
                base64.urlsafe_b64encode(
                    oss2.compat.to_bytes(bucket_name)
                    )
                )
            )
        bucket.process_object(str_result, process)

    except oss2.exceptions.NoSuchKey as e:
        return ''

    except Exception as e:
        #If there is a problem with the thumbnail generation,
        #our code is wrong
        if index+1 == tot_img_objs:
            #To-do 
            #retry thumbnail creation
            #Send email to the developers
            logging.error(e)
            messages.error(
                request, f"We are having difficulty processing your image(s), \
                check your post if everything is fine.")

        img_obj.image_thumb = str_result
        if img_mid_name:
            img_obj.image_mid_size = str_result
        img_obj.save()
        saved_objs += 1
        continue

    else:
        img_obj.image_thumb = thumb_name
        if saved_objs == 0:
            obj.thumbnail = thumb_name
            obj.save()
        if img_mid_name:
            img_obj.image_mid_size = img_mid_name
        img_obj.save()
        saved_objs += 1
