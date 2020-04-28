import datetime
cur = datetime.datetime(2019, 12, 1)
res = open("res.csv", "w")
totdic = {}
while cur <= datetime.datetime.today():
    try:
        lines = open(f"{cur:%Y%m%d}.txt", encoding="utf-8").readlines()
        dic = dict([i.split() for i in lines])
        totdic[f"{cur:%Y%m%d}"] = dic
    except FileNotFoundError as e:
        print(e)
        pass
    cur = cur + datetime.timedelta(days=1)
keys = set()
for i in totdic.values():
    keys |= set(i.keys())
with open("res.csv", "w") as f:
    print("," + ",".join(keys), file=f)
    for date, dic in totdic.items():
        print(date, end=",", file=f)
        for k in keys:
            print(dic.setdefault(k, 0), end=",", file=f)
        print("", file=f)
