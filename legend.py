import requests
import re


class group():
    def __init__(self):
        self.songs = {}

    def get_all(self):
        data = {}
        for name, av in self.songs.items():
            with requests.get(f"http://api.bilibili.com/archive_stat/stat?aid={av}") as u:
                data[name] = int(re.findall("(?<=\"view\":)\d+", u.text)[0])
        return data


def make_groups():
    groups = {}
    with open("config.txt", "r", encoding="utf-8") as config:
        lines = config.readlines()
    lines = [line.split() for line in lines]
    for l in lines:
        if l[0] == "Group":
            cur = group()
            groups[l[1]] = cur
        if l[0] == "Goal":
            cur.goal = int(l[1])
        if l[0] == "Song":
            cur.songs[l[1]] = int(l[2])
    return groups


def get_from_file(date):
    with open(f"history//{date}.txt", "r", encoding="utf-8") as hist:
        lines = hist.readlines()
    lines = [line.split() for line in lines]
    data = {}
    for l in lines:
        data[l[0]] = int(l[1])
    return data


def save_as_file(dict, date):
    with open(f"history//{date}.txt", "a", encoding="utf-8") as save:
        for name, view in dict.items():
            print(name, view, file=save)


if __name__ == "__main__":
    groups = make_groups()
    # for key in groups.keys():
    #     data = groups[key].get_all()
    #     print(data)
    hist = get_from_file("20191201")
