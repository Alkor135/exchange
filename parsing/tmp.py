import datetime

# today = datetime.datetime(2022, 5, 22)
# today.get_weekday()  # what I look for

ans = datetime.date(2022, 5, 22)
print(ans.strftime("%A"))
