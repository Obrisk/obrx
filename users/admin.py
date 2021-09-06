from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import User, WechatUser

@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    ordering = ('-date_joined', )
    fieldsets = (
            ('User Profile',
                {'fields':
                    ('name', 'is_official', 'is_seller', 'points', 'city',
                        'province_region', 'country', 'phone_number', 'picture',
                        'thumbnail', 'org_picture', 'linkedin_account', 'wechat_id', 'notes',
                        'english_address', 'chinese_address', 'gender', 'wechat_openid',
                    )
                }
            ),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'last_login', 'date_joined',
        'city', 'province_region', 'thumbnail', 'points')
    search_fields = ['username', 'phone_number', 'email', 'city']
    #readonly_fields = ('phone_number',)


admin.site.register(WechatUser)
