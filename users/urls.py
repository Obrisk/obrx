from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'),

    url(regex=r'^social-form-final/$',
        view=views.SocialPostView.as_view(),
        name='social_final_form'),

    url(regex=r'^signup/$',
        view=views.EmailSignUp.as_view(),
        name='email_signup'),

    url(regex=r'^wx-auto-login-149eb8766awswdff224fgo029k12ol8/$',
        view=views.wechat_auto_login,
        name='wx_auto'),

    url(regex=r'^update-profile-pic/$',
        view=views.update_profile_pic,
        name='update_profile_pic'),

    url(regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'),

    url(regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'),

    url(regex=r'^i/(?P<rq_user>[\w.@+-]+)/$',
        view=views.user_classifieds_list,
        name='user_classifieds'),

    url(regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'),
]
