import os
import random

import pytest
import allure

from Common.Assert import Assert
from Common.Log import Log
from Common.Base import Base
from Conf.Config import Config

base_path = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(base_path, "..", "Data", "test.yaml"))
obj = Config(path)
test_data = obj.test_data(path)


def add(a, b):
    return a + b


class TestApi:
    @pytest.fixture(scope="class", autouse=True)
    def class_logging(self):
        Log.logger("Start Class...")
        yield
        Log.logger("Finish Class...")

    @pytest.fixture(autouse=True)
    def method_logging(self):
        Log.logger("Start Method...")
        yield
        Log.logger("Finnish Method...")

    @pytest.mark.parametrize("name,method, url, headers, params, expected, export", test_data)
    def test_api(self, name, method, url, headers, params, expected, export):
        allure.dynamic.title("请求接口:{i}".format(i=url))  # 设定用例标题
        allure.dynamic.description("用例描述:{i}".format(i=name))  # 设定用例描述
        # com_flag = True    # 设置默认的断言结果
        headers = obj.get_var(headers)    # 判断请求头中是否有变量,有的话需获取变量值
        Log.logger("Request Headers:"+str(headers))
        params = obj.get_var(params)    # 判断请求消息体中是否有变量,有的话需获取变量值
        Log.logger("Request Body:"+str(params))
        if method == "GET":
            data = Base.base_request(url=url, method=method, headers=headers, params=params)
        elif method == "POST":
            data = Base.base_request(url=url, method=method, headers=headers, data=params)
        Log.logger("Response Headers:" + str(data.headers))
        Log.logger("Response Body:" + str(data.text))
        if export == "NULL":      # 接口返回是否需要输出变量供其他接口使用
            pass
        else:
            obj.set_var(path, export, data)
        com_flag = Assert.assertion(data,expected)

        assert data.status_code == 200, "Test Failed!!!"
        assert com_flag, "Test Failed!!!"

    @pytest.mark.parametrize("a,b,expected", [(5, 7, 9),
                                              (4, 4, 8),
                                              (9, 9, 18),
                                              (40, 40, 1),
                                              (6, 5, 30)])
    def test_add(self, a, b, expected):
        sum = add(a, b)
        assert expected == sum, "Test Failed!!!"
