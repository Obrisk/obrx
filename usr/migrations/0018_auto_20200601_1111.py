# Generated by Django 2.2.11 on 2020-06-01 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_openid',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='wechat_openid'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_unionid',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='wechat_unionid'),
        ),
    ]