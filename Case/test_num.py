import os

import pytest
import allure
import logging

from Common.Assert import Assert
from Common.Base import Base
from Conf.Config import Config

# logging.basicConfig(level=logging.INFO)
base_path = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(base_path, "..", "Data", "test.yaml"))
obj = Config()
data = obj.test_data(path)
re = Base()


# aes =


def add(a, b):
    return a + b


class TestApi:
    @pytest.fixture(scope="class", autouse=True)
    def class_logging(self):
        logging.info("Start Class...")
        yield
        logging.info("Finish Class...")

    @pytest.fixture(autouse=True)
    def method_logging(self):
        logging.info("Start Method...")
        yield
        logging.info("Finnish Method...")

    @pytest.mark.parametrize("a,b,expected", [(5, 7, 9),
                                              (4, 4, 8),
                                              (9, 9, 18),
                                              (40, 40, 1),
                                              (6, 5, 30)])
    def test_add(self, a, b, expected):
        sum = add(a, b)
        logging.info("Test_num...")
        assert expected == sum, "Test Failed!!!"
