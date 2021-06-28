# -*- coding:utf-8 -*-
import json
import os
from hashlib import md5
from io import IOBase
from pathlib import Path

import yaml

time_format = "%Y-%m-%d %H:%M:%S"


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            return del_file(file_path)


def get_dict_value_by_dot(dt, str_with_dot: str):
    """
    以properties配置文件的方式,以点号分隔key获取配置文件value
    :return:
    """
    # 如果字段为空直接返回
    if not dt:
        return None

    if "." not in str_with_dot:
        return dt[str_with_dot] if str_with_dot in dt else None
    else:
        i = str_with_dot.index(".")
        k = str_with_dot[0:i]
        return get_dict_value_by_dot(dt[k], str_with_dot[i + 1:])


def get_dict_value_by_key_list(dt, keyList):
    """
    根据Key列表从字典中获取数据
    :param dt:
    :param keyList:
    :return:
    """
    if not keyList:
        return dt
    else:
        for i in range(len(keyList)):
            key = keyList[i]
            if dt.__contains__(key):
                return get_dict_value_by_key_list(dt[key], keyList[i + 1:])
            else:
                return None


def find_relative_path(relative_path, parent_path=Path(__file__)):
    """
    解析配置文件路径

    在不同的脚本中执行会
    导致相对路径找不到文件
    可以调用此方法
    :param parent_path:
    :param relative_path:
    :return:
    """

    rp = Path(relative_path)

    if parent_path.joinpath(rp).is_file():
        return parent_path.joinpath(rp).absolute()
    else:
        return find_relative_path(relative_path, parent_path.parent)


def save_file(obj: object, file_path: str, write_mode="w"):
    """
    save object to file
    object can be list, dict, json, str,
    if object is entity it must be serializable
        eg: clz.__dict__

    :param write_mode: w, wb
    :param obj:
    :param file_path: absolute file path
    :return:
    """
    p = Path(file_path)
    p.parent.absolute().mkdir(parents=True, exist_ok=True)
    s = p.suffix[1:]
    file_type = "yaml" if s in ["yaml", "yml"] else "json"

    if not isinstance(obj, (str, list, tuple, dict)):
        obj = obj.__dict__

    if "json" == file_type:
        with open(file_path, write_mode, encoding="utf-8") as f:
            json.dump(obj, f, indent=4)
    elif "yaml" == file_type:
        with open(file_path, write_mode, encoding="utf-8") as f:
            yaml.dump(obj, f, indent=4)
    return True


def load_file(file_path: str, clz=dict):
    """
    read file to python object
    default dict, list, str

    also you can specify entity
    :param file_path:
    :param clz:
    :return:
    """
    p = Path(file_path)
    s = p.suffix[1:]
    file_type = "yaml" if s in ["yaml", "yml"] else "json"

    dt = dict()

    if not p.is_file():
        return none_type(clz)
    size = os.path.getsize(p.absolute())

    if size == 0:
        return none_type(clz)

    if "json" == file_type:
        with open(p.absolute(), "r", encoding="utf-8") as fp:
            dt = json.load(fp)
    elif "yaml" == file_type:
        with open(p.absolute(), "r", encoding="utf-8") as fp:
            dt = yaml.load(fp, Loader=yaml.FullLoader)

    if clz and dt and clz not in [dict, list, tuple, str, int, float, bool]:
        return clz(**dt)
    return dt


def none_type(class_type=str):
    """
    return specity type empty
    dict --> {}
    list --> []
    tuple --> ()
    other --> None
    :param class_type:
    :return:
    """
    if class_type == dict:
        return dict()

    if class_type == list:
        return list()

    if class_type == tuple:
        return tuple()

    return None


def update_entity(obj, dt: dict):
    """
    update entity by dict
    if key is id, pass
    if value is empty, pass
    :param obj:
    :param dt:
    :return:
    """
    id_list = [
        "id", "uuid", "aid", "bid", "cid", "did", "eid", "fid", "gid", "hid", "iid", "jid", "kid", "lid",
        "mid", "nid", "oid", "qid", "rid", "sid", "tid", "uid", "vid", "wid", "xid", "yid", "zid"
    ]
    for k, v in dt.items():
        if hasattr(obj, k) and k not in id_list:
            if isinstance(v, int):
                setattr(obj, k, v)
                continue

            if v:
                setattr(obj, k, v)

    return obj


def test():
    # print(find_relative_path("config/logger.yml"))

    # save_file({"aa": 11, "bc": 22}, "temp/test.txt")
    # save_file({"aa": 11, "bc": 22}, "temp/test.txt", write_mode="a")
    # save_file("sdf", "temp/test.txt", write_mode="a")
    # save_file(["abc", "sdf", "jkl"], "temp/test.txt", write_mode="a")
    # save_file((123, 234, 345), "temp/test.txt", write_mode="a")
    # save_file(Message(), "temp/test.txt", write_mode="a")
    # save_file(Message(), "temp/test.txt")

    # print(load_file("temp/test.txt", clz=Message).uuid)
    # print(load_file("temp/test.txt"))
    print(get_dict_value_by_dot(load_file("../config/engine-main.yml"), "config.server.is_config_center"))


if __name__ == '__main__':
    test()
