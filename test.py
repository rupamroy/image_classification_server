from datetime import datetime, timedelta


def weekendSpecial():
    weekday = datetime.now().weekday()
    # if sunday or saturday
    weekdayExcuse = True if ( weekday == 5 or weekday == 6) else False
    hour = datetime.now().hour
    hoursOnWeekday = True if (hour >= 7 and hour < 16) else False
    return (weekdayExcuse and hoursOnWeekday)



if weekendSpecial():
    print('Hi')