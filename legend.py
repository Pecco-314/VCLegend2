import datetime
import re
import requests
import pyperclip
import os


def get_formatted_date(delta: int = 0) -> str:
    """
    由向前偏移量得到标准日期字符串

    例如，如果date是表示当前时间的datetime变量，而delta为1，那么将返回昨天的日期字符串，格式为YYYYmmdd
    """
    return f"{(datetime.datetime.today()-datetime.timedelta(days=delta)):%Y%m%d}"


def sub_dict(dic1: dict, dic2: dict) -> dict:
    """
    将两个字典键相同的元素相减

    如果一个键在dic1中存在，而在dic2中不存在，则保留该键对应的值，
    如果一个键在dic2中不存在，而在dic2中存在，则不保留该键对应的值

    例如，dic1是{'A':100, 'B':200}，dic2是{'B':50, 'C':100}，则应当返回{'A':100, 'B':150}
    """
    dic = {}
    for key in dic1.keys():
        try:
            dic[key] = dic1[key] - dic2[key]
        except KeyError:  # 如果dic2中不存在该键，视为0
            dic[key] = dic1[key]
    return dic


def get_from_file(date: str) -> dict:
    """从文件中读取数据，存入字典"""
    with open(f"history//{date}.txt", "r", encoding="utf-8") as hist:
        lines = hist.readlines()
    lines = [line.split() for line in lines]
    data = {}
    for l in lines:
        data[l[0]] = int(l[1])
    return data


def save_as_file(dic: dict, date: str):
    """把以字典形式储存的数据保存到指定日期对应的文件中"""
    with open(f"history//{date}.txt", "a", encoding="utf-8") as save:
        for name, view in dic.items():
            print(name, view, file=save)


class video():
    """
    B站视频
        av：视频的av号
    """

    def __init__(self, av: str):
        self.av = av

    def get_views_from_api(self):
        """从api中获取播放量"""
        self.latter = get_formatted_date()
        with requests.get(f"http://api.bilibili.com/archive_stat/stat?aid={self.av}") as u:
            # 利用正则表达式，找到"views": 后的数字即为播放量
            self.views = int(re.findall("(?<=\"view\":)\\d+", u.text)[0])


class videogroup():
    """
    视频组
        goal：目标播放量
        congrats：祝贺语，在达到目标播放量后显示
        videos：一个字典，键为视频的名称，值为video对象
    """

    def __init__(self, goal: int = 0, congrats: str = "恭喜！"):
        self.goal = goal
        self.congrats = congrats
        self.videos = {}

    def set_views(self, date: str = get_formatted_date(), data: dict = None):
        """对于一个视频组的所有视频而言，都使用api或字典更新播放量"""
        if data:
            for name, view in data.items():
                try:  # 原视频组中没有的就不更新
                    self.videos[name].views = view
                except KeyError:
                    continue
        else:
            for video in self.videos.values():
                video.get_views_from_api()
            save_as_file(self.get_views(), date)

    def get_views(self) -> dict:
        """获取视频播放量数据，返回字典"""
        data = {}
        for name, video in self.videos.items():
            data[name] = video.views
        return data


def make_groups() -> dict:
    """根据config文件创建视频组字典"""
    groups = {}
    with open("config.txt", "r", encoding="utf-8") as config:
        lines = config.readlines()
    lines = [line.split() for line in lines]
    for l in lines:
        if l[0] == "Group":  # 命令Group：创建新组
            cur = videogroup()
            groups[l[1]] = cur
        elif l[0] == "Goal":  # 命令Goal：设置视频组的目标播放量
            cur.goal = int(l[1])
        elif l[0] == "Congrats":  # 命令Congrats：设置视频组的祝贺语
            cur.congrats = l[1]
        elif l[0] == "Video":  # 命令Video：添加视频
            cur.videos[l[1]] = video(l[2])
    return groups


def get_delta(former: str, latter: str, delta_days: int, group: videogroup) -> tuple:
    """
    得到某个视频组的所有视频在两个日期前后的增量，并估计达到目标的时间，返回增量和估计时间所组成的元组
    """
    hist = get_from_file(former)
    if latter == "api":  # 从api中获取数据
        group.set_views()
        data = group.get_views()
    else:
        data = get_from_file(latter)
        group.set_views(data=data)
    delta = sub_dict(data, hist)
    predict = {}
    for name in group.videos.keys():
        rest = group.goal - data[name]
        predict[name] = rest*delta_days//delta[name]
    return delta, predict


def get_brief(former: str = get_formatted_date(1), latter: str = "api", delta_days: int = 1, titled=True) -> str:
    """
    生成简报字符串
        former：较早的日期，应传入日期字符串，如"20191201"
        latter：较近的日期，应传入日期字符串或"api"，表示数据从api中获取
        delta_days：日期的间隔
        titled：是否显示标题
    """
    groups = make_groups()
    is_first = True
    if titled:
        t = datetime.datetime.today()
        s = f"每日简报 {t:%#m}月{t:%#d}日\n"
    else:
        s = ""
    for g in groups.values():
        if is_first:
            is_first = False
        else:
            s = s + ("----\n")
        delta, predict = get_delta(former, latter, delta_days, g)
        # 按天数从低到高排序
        for key in sorted(predict.keys(), key=lambda k: predict[k]):
            s = s + f"{key}：播放量{g.videos[key].views}，增量{delta[key]}"
            if g.videos[key].views > g.goal:
                s = s + f"（{g.congrats}）\n"
            else:
                s = s + f"（{predict[key]:d}天）\n"
    pyperclip.copy(s)  # 粘贴到剪切板
    return s


if __name__ == "__main__":
    print(get_brief())
    os.system("pause")
