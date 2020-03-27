import json
from Common.Log import Log
from Conf.Config import Config


class Assert:

    @classmethod
    # 校验某个字段是否相等
    def eq_assert(self, data, expected):
        expected = expected
        if expected[0] == "code":
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=data.status_code))
            if data.status_code == expected[1]:
                return True
            else:
                return False

        if "headers" in expected[0]:
            headers = data.headers
            temp = expected[0].split('.')
            for i in range(1, len(temp)):
                str = temp[i]
                text = headers[str]
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=text))
            if text == expected[1]:
                return True
            else:
                return False

        if "body" in expected[0]:
            body = data.text
            # if (type(body).__name__=='dict'):    # 判断是否为字典
            if isinstance(body, dict):  # 判断是否为字典
                pass
            else:
                body = json.loads(body)  # 字符串转换成字典
            temp = expected[0].split('.')
            for i in range(1, len(temp)):
                str = temp[i]
                text = body[str]
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=text))
            if text == expected[1]:
                return True
            else:
                return False

    @classmethod
    # 校验某个字段是否包含某字符串
    def co_assert(self, data, expected):
        if expected[0] == "code":
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=data.status_code))
            if data.status_code in expected[1]:
                return True
            else:
                return False

        if "headers" in expected[0]:
            headers = data.headers
            temp = expected[0].split('.')
            for i in range(1, len(temp)):
                str = temp[i]
                text = headers[str]
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=text))
            if expected[1] in text:
                return True
            else:
                return False

        if "body" in expected[0]:
            body = data.text
            # if (type(body).__name__ == 'dict'):  # 判断是否为字典
            if isinstance(body, dict):  # 判断是否为字典
                pass
            else:
                body = json.loads(body)  # Json字符串转换成字典
            temp = expected[0].split('.')
            for i in range(1, len(temp)):
                str = temp[i]
                text = body[str]
            Log.logger("Expected_value: {a}".format(a=expected[1]))
            Log.logger("Actual_value: {a}".format(a=text))
            if text in expected[1]:
                return True
            else:
                return False

    @classmethod
    # 校验某个字段是否不相等
    def nq_assert(self, data, expected):
        result = self.eq_assert(data, expected)
        return ~result

    @classmethod
    # 多种断言的集合
    def assertion(self, data, expected):
        result = []
        com_flag = True
        for i in expected:     # 校验接口返回,返回结果是一个以True或False的列表
            for k, v in i.items():
                if k == "eq":
                    Log.logger("Equal Assert!!! Expected_value =Actual_value ... ")
                    flag = self.eq_assert(data, v)
                    result.append(flag)
                elif k == "co":
                    Log.logger("Contain Assert!!! Actual_value contains Expected_value ... ")
                    flag = self.co_assert(data, v)
                    result.append(flag)
                elif k == "nq":
                    Log.logger("Not Equal Assert!!! Expected_value !=Actual_value ... ")
                    flag = self.nq_assert(data, v)
                    result.append(flag)
        for i in result:     # 对断言列表进行校验,只要含有Flase测试结果就为False
            if i == False:
                com_flag = False
                break
        return com_flag
