"""
单元测试数据模拟工厂
"""

import datetime

import faker
from django.contrib.auth.models import UserManager
from django.utils import timezone
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker("zh_CN")


# flake8: noqa F401


class UserFactory(DjangoModelFactory):
    phone = Faker("phone_number")
    openid = "test_openid"

    class Meta:
        model = UserManager

    # 对象创建后调用方法
    @post_generation
    def channels(self, create, extracted):
        pass
        # if not create:
        #     return
        #
        # if extracted:
        #     for channel in extracted:
        #         UserChannel.objects.create(channel=channel, user=self)
