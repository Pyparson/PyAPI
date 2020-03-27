import json
import re

import yaml
import os

from Common.Log import Log


class Config:
    def __init__(self,path):
        global var
        with open(path, 'r') as f:
            temp = yaml.safe_load(f)
        var = temp["Var"]


    base_path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_path, "config.yaml"))
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    env = data["ENV"]
    # global var
    # with open(path, 'r') as f:
    #     temp = yaml.safe_load(f)
    # var = temp["Var"]


    @classmethod
    def get_config(self):
        # 获取环境配置
        # conf = None
        if self.env == "Debug":
            conf = self.data["Debug"]
        elif self.env == "Release":
            conf = self.data["Release"]
        else:
            raise ("There are something error!!!Pls check it...")

        return conf

    @classmethod
    def get_case(self, path):
        test_list = []
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        case = data["Case"]
        for a in case:
            for k, v in a.items():
                if k == "Test":
                    test_list.append(v)
        return test_list

    @classmethod
    def get_case_name(self, path):
        data = self.get_case(path)
        url_li = []
        for i in data:
            if "name" not in i.keys():
                i["name"] = "NULL"
            for k, v in i.items():
                if "name" == k:
                    url_li.append(v)
        return url_li

    @classmethod
    def get_method(self, path):
        data = self.get_case(path)
        method_li = []
        for i in data:
            re = i["request"]
            for k, v in re.items():
                if k == "method":
                    method_li.append(v)
        return method_li

    @classmethod
    def get_headers(self, path):
        data = self.get_case(path)
        headers_li = []
        for i in data:
            re = i["request"]
            for k, v in re.items():
                if k == "headers":
                    headers_li.append(v)
        return headers_li

    @classmethod
    def get_params(self, path):
        data = self.get_case(path)
        params_li = []
        for i in data:
            re = i["request"]
            for k, v in re.items():
                if k == "params":
                    params_li.append(v)
        return params_li

    @classmethod
    def get_url(self, path):
        conf = self.get_config()
        data = self.get_case(path)
        url_li = []
        if "base_url" in conf.keys():
            for i in data:
                re = i["request"]
                for k, v in re.items():
                    if k == "URL":
                        value = conf["base_url"] + v
                        url_li.append(value)
        else:
            for i in data:
                re = i["request"]
                for k, v in re.items():
                    if k == "URL":
                        url_li.append(v)
        return url_li

    @classmethod
    def get_validate(self, path):
        data = self.get_case(path)
        validate_li = []
        for i in data:
            re = i["validate"]
            validate_li.append(re)
        return validate_li

    @classmethod
    def get_export(self, path):
        data = self.get_case(path)
        export_li = []
        for i in data:
            if "export" in i.keys():
                value = i["export"]
            else:
                value = "NULL"
            export_li.append(value)
        return export_li

    @classmethod
    def test_data(self, path):
        name = self.get_case_name(path)
        method = self.get_method(path)
        url = self.get_url(path)
        headers = self.get_headers(path)
        params = self.get_params(path)
        validate = self.get_validate(path)
        export = self.get_export(path)
        # data = [(a, b, c, d, e) for a, b, c, d, e in
        #         zip( method, url, headers, params, validate)]  # 长度相同的几个列表组合成一个
        # data = [(a, b, c, d, e, f) for a, b, c, d, e, f in
        #         zip(name, method, url, headers, params, validate)]  # 长度相同的几个列表组合成一个
        data = [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in
                zip(name, method, url, headers, params, validate, export)]  # 长度相同的几个列表组合成一个
        return data

    @classmethod
    # 设定全局变量值
    def set_var(self, path, di, res):
        for k, v in di.items():
            if "headers" in v:
                headers = res.headers
                temp = v.split('.')
                for j in range(1, len(temp)):
                    str = temp[j]
                    text = headers[str]
            elif "body" in v:
                body = res.text
                if isinstance(body, dict):  # 判断是否为字典
                    pass
                else:
                    body = json.loads(body)  # Json字符串转换成字典
                temp = v.split('.')
                for j in range(1, len(temp)):
                    str = temp[j]
                    text = body[str]
            di[k] = text
        var.update(di)
        Log.logger("Global Var:"+json.dumps(var))
        # print("设定全局变量"+var)
        return var

    @classmethod
    def get_var(self,di):
        for k, v in di.items():
            if "${" in v:
                variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
                m = variable_regex_compile.search(v)
                l = m.group().split('{')[-1].split('}')[0]
                di[k] = v.replace(m.group(), str(var[l]))
        return di

    # def get_var(self,di):


if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_path, "config.yaml"))
    # print(Config.set_variable(path))
    print(Config.get_export(path))
