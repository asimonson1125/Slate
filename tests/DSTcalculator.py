import datetime

year = 2021
today = datetime.date(year, 3, 1)
print("first of March day of week: " + str(today.isoweekday())) # Sunday = 7, Monday = 1
endDST = today.replace(day=15-today.isoweekday())
print("Daylight savings starts on: " + str(endDST))

today = datetime.date(year, 11, 1)
print("first of November day of week: " + str(today.isoweekday())) # Sunday = 7, Monday = 1
endDST = today.replace(day=8-today.isoweekday())
print("Daylight savings ends on: " + str(endDST))