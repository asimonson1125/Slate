import datetime

start = datetime.date(2020,1,1)
end = datetime.date(2022, 5, 1)
today = datetime.date(start.year-1, 3, 1)
dates = []
while(today < end):
    today = today.replace(year=today.year+1, month=3, day=1)
    startDST = today.replace(day=15-today.isoweekday())
    # print("Daylight savings starts on: " + str(endDST))

    today = today.replace(month=11, day=1)
    endDST = today.replace(day=8-today.isoweekday())
    # print("Daylight savings ends on: " + str(endDST))
    dates.append([startDST, endDST])

print(1)