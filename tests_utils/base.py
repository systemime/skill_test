import copy
import json
import os
from pathlib import Path
from typing import Union
from unittest import mock

import ujson
from django.core import mail
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.test.client import Client
from django.test.testcases import TransactionTestCase
from django.urls import reverse
from openpyxl import load_workbook
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests_utils.factories import UserManager

import_path = Path(__file__).resolve(strict=True).parent / "import_file"


# pylint:disable=R0903,E1120
# flake8: noqa F401,B950


class SKTestCase(TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.original_client = cache.client.get_client()
        self.__patchers = {}

    def tearDown(self):
        super().tearDown()
        # TODO: 事务测试调节下，测试结束登陆会被自动清理
        # self.c.logout()

        for p in self.__patchers.values():
            p.stop()

    def patch_once(self, spec, *args, **kwargs):
        """mock 该对象并在测试完停止"""

        patcher = mock.patch(spec, *args, **kwargs)
        mock_obj = patcher.start()
        self.__patchers[mock_obj] = patcher
        return mock_obj

    @property
    def signed_api_client(self, *args, **kwargs) -> APIClient:
        """返回一个已签名的客户端"""

        # TODO eg.
        user = kwargs["user"]

        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION=f"AutoButler {str(RefreshToken.for_user(user))}",
            HTTP_X_AutoButler_Channel="xxx",
        )
        return client

    @property
    def logging_client(self, test_user=None) -> APIClient:
        """返回一个基于django admin的登陆客户端"""

        password = "test_user"
        client = APIClient(enforce_csrf_checks=False)

        if not test_user:
            test_user = UserManager.objects.create_superuser(
                username="test_user",
                email="test@gmail.com",
                password=password,
            )

        self.test_user = test_user
        client.login(username=self.test_user.username, password=password)

        return client

    def cache_delete(self, key):
        if not key:
            raise Exception("参数 key 不能为空")
        self.original_client.delete(key)

    @staticmethod
    def _locate_test_dir(file_name):
        dat_pth = os.path.join(os.path.dirname(__file__), "test_files")
        return os.path.join(dat_pth, file_name)

    def load_file(self, file_name):
        """加载一个文件
        测试文件同级目录下必须存在 test_files 文件夹
        """
        with open(self._locate_test_dir(file_name)) as f:
            return f.read()

    def load_json_file(self, file_name):
        """加载一个json文件
        测试文件同级目录下必须存在 test_files 文件夹
        """
        with open(self._locate_test_dir(file_name)) as f:
            return ujson.load(f)

    @staticmethod
    def warp_update_file(file_path, need_bak=False, excel_obj=False):
        """
        包装一个测试上传的上传对象
        file_path
        如果需要返回测试文件对象，need_bak=True
        如果测试上传excel并要返回excel解析对象，excel_obj=true
        """
        file = Path(file_path)
        with open(file_path, "rb") as fb:
            update_file = SimpleUploadedFile(file.name, fb.read())

        result = [update_file]

        if need_bak:
            result.append(copy.deepcopy(update_file))

        if excel_obj:
            excel_file = copy.deepcopy(update_file)
            wb = load_workbook(filename=excel_file, data_only=True)
            sheet = wb.active
            result.append(sheet)

        return result
