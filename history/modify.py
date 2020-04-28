import datetime


def modify(filename, old, new):
    with open(filename, "r", encoding="utf-8") as f:
        s = f.read()
        s = s.replace(old, new).strip()
    print(s, file=open(filename, "w", encoding="utf-8"))


cur = datetime.datetime(2019, 12, 1)
while cur <= datetime.datetime.today():
    try:
        modify(f"{cur:%Y%m%d}.txt", "饭圈小姐", "饭姐")
    except FileNotFoundError as e:
        print(e)
        pass
    cur = cur + datetime.timedelta(days=1)
