import datetime
import numpy as np

TIME_BREAKFAST = "9:30"     # breakfast time in the morning
TIME_LUNCH = "11:30"        # lunch time in the midday

DURATION_BREAKFAST = "0:15" # Breakfast break 
DURATION_LUNCH = "0:30"     # Lunch break


def get_time():
    """
    returns the current time in the format "HH:MM"
    """
    return datetime.datetime.now().strftime("%H:%M")


def get_date(yesterday=False):
    """
    returns the current date in the form YYYY-MM-DD
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if yesterday:
        date_split = date.split('-')
        if int(date_split[-1]) > 1:
            date_split[2] = str(int(date_split[-1])-1)
        else:
            date_split[2] = str(30)
        date = '-'.join(date_split)
    return date


def get_daily_work_hour(worktime, workdays=5):
    """
    calculates the average hours which you have to work daily to achieve the
    weekly goal of hours. Updates with every worked day.

    Parameters
    ---------- 
    worktime : str - hh:mm
        the time which you alreay worked.
    workdays : int, optional
        number of days you work. The default is 5.

    Returns
    -------
    str - hh:mm
        the average time per day.

    """
    hours, mins = split_time(worktime)
    hours_daily = int(np.floor(hours/workdays))
    mins_daily = round(mins/workdays + (hours/workdays - hours_daily)*60)
    return f'{formate_clock(hours_daily)}:{formate_clock(mins_daily)}'


def get_time_pause(start, **kwargs):
    """
    Calculates the current pause while the working

    Parameters
    ----------
    start : TYPE
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    pause : TYPE
        DESCRIPTION.

    """
    time_now = datetime.datetime.now().strftime("%H:%M")
    lunch = False
    pause = '0:00'
    
    if not is_later(start, TIME_BREAKFAST) and is_later(time_now, TIME_BREAKFAST):
        if not is_later(pause, DURATION_BREAKFAST) and not is_later(get_time_dif(time_now, TIME_BREAKFAST), DURATION_BREAKFAST):
            pause = get_time_dif(time_now, TIME_BREAKFAST)
        else: 
            pause = DURATION_BREAKFAST
            
    for key, value in kwargs.items():
        if key == 'lunch_pause':
            pause = get_time_sum(pause, value)
            lunch = True
    if not lunch and not is_later(start, TIME_LUNCH) and is_later(time_now, TIME_LUNCH):
        if not is_later(pause, DURATION_LUNCH) and not is_later(get_time_dif(time_now, TIME_LUNCH), DURATION_LUNCH):
            pause = get_time_sum([pause, get_time_dif(time_now, TIME_LUNCH)])
        else: 
            pause = get_time_sum([pause, DURATION_LUNCH])
    return pause


def get_work_hour(start):
    """
    calculates the hours which are worked up to now

    Parameters
    ----------
    start : str
        start time - hh:mm.
        

    Returns
    -------
    str
        the hours - hh:mm.

    """
    time_now = datetime.datetime.now().strftime("%H:%M")
    pause = get_time_pause(start)
    return get_time_dif(time_now, [start, pause])


def get_end_work(current_worktime, worktime):
    """
    calculates the time of the end of the work

    Parameters
    ----------
    current_worktime : TYPE
        DESCRIPTION.
    worktime : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    # print(current_worktime, worktime)
    start = get_time_dif(current_worktime, 
                         datetime.datetime.now().strftime("%H:%M"))
    
    cur_pause = get_time_pause(start)
    time_pause = get_time_dif(cur_pause, get_time_sum([DURATION_BREAKFAST, 
                                                       DURATION_LUNCH]))
    
    # print(cur_pause, current_worktime, datetime.datetime.now().strftime("%H:%M"))
    if not is_later(current_worktime, worktime):
        time_now = datetime.datetime.now().strftime("%H:%M")
        time_left = get_time_dif(worktime, current_worktime)
        # print(time_now, time_left, time_pause)
        return get_time_sum([time_now, time_left, time_pause])
    else:
        return "Done!"


def formate_clock(value):
    """
    formates the representation of the mins/hours. In case you get a single 
    digit time, it adds a '0' in front of them.

    Parameters
    ----------
    value : int
        Integer in the range between 0 and 60.

    Returns
    -------
    string
        String which represents the value of the time between 00 and 60, with
        better fromation.

    """
    if value < 10:
        return f'0{value}'
    else:
        return str(value)
        
    
def split_date_time(time: str):
    if time_1.find('T'):
        return time_1.split('T')
    else:
        return time_1, None
    

def is_later_time(time_1: str, time_2: str) -> bool:
    hours_1, mins_1 = split_time(time_1)
    hours_2, mins_2 = split_time(time_2)

    # compares if time_1 is before time_2 or later
    if hours_1 < hours_2:
        return False

    if hours_1 == hours_2 and mins_1 < mins_2:
        # when the time is equal -> True
        return False
    return True
        

def is_later_date(date_1: str, date_2: str) -> bool:
    """checks if date_1 is later then date_2

    Args:
        date_1 (str): date in form dd-mm-yyyy
        date_2 (str): date in form dd-mm-yyyy

    Returns:
        bool: True when later, False rest
    """
    
    year_1, month_1, day_1 = split_date(date_1)
    year_2, month_2, day_2 = split_date(date_1)
    
    if year_1 < year_2:
        return False
    
    if month_1 < month_2:
        return False
    
    if month_1 == month_2 and day_1 <= day_2:
        return False
    
    return True


def is_later(time_1, time_2) -> bool:
    """
        compares time_2 with time_1 --> True when time_1 is after time_2
        time_1: str, format HH:MM
        time_2: str, format HH:MM
        return: bool
    """
    if time_1 is None or time_2 is None:
        return False
    
    if isinstance(time_2, list):
        comp_list: list = []
        for item in time_2:
            comp_list.append(is_later(time_1, item))
        
        if all(comp_list):
            return True
        else:
            return False
    else:

        time_1_time, time_1_date = split_date_time(time_1)
        time_2_time, time_2_date = split_date_time(time_2)
        
        if time_1_date is not None and time_2_date is not None:
            # if a date is given check if it's today or tomorrow
            if not is_today() and is_later_date(time_1_date, time_2_date):
                # if it's not today -> some before or after AND later -> date is later then the other -> time doesn not matter anymore
                    return True
                
        # if no date given -> check only for the time
        return is_later_time(time_1_time, time_2_time)


def is_today(date_1, date_2):
    if date_1 is None or date_2 is None:
        return False
    year_1, month_1, day_1 = split_date(date_1)
    year_2, month_2, day_2 = split_date(date_2)

    if year_1 != year_2 or month_1 != month_2 or day_1 != day_2:
        return False
    else:
        return True


def get_calc_mins(diff_hours, mins_1, mins_2):
    """
    calculates the difference in the minutes. It'll be executed twice when 
    calculating the difference in hours/mins. -> own function

    Parameters
    ----------
    diff_hours : int
        number between 0 and 23.
    mins_1 : int
        number between 0 and 59.
    mins_2 : int
        number between 0 and 59.

    Returns
    -------
    diff_hours : int
        number between 0 and 23.
    diff_mins : int
        number between 0 and 59.

    """
    if mins_1 > mins_2:
        diff_mins = mins_1 - mins_2
    else:
        # if mins_1 smaller, then there is no full hour between both
        # times and you have to calc the difference between mins_1 to the 
        # full 60 minutes and the add the mins_1 for the real difference
        
        if diff_hours == 0:
            # in the case that 0:xx - 0:xx should be calculated, then is 
            # order of the calculation the normal without referencing on the 60
            diff_mins = mins_2 - mins_1
            
        else:             
            mins_to_60 = 60 - mins_2
            diff_mins = mins_1 + mins_to_60
            
            if diff_mins == 60:
                # If the difference is 60 - zero it and don't subtract the hours
                diff_mins = 0 
            else:    
                diff_hours -= 1     # there is no full hour difference -> sub 1
    return diff_hours, diff_mins


def get_calc_dif(hours_1, mins_1, hours_2, mins_2):
    """
    calculates the difference between the hours and minutes

    Parameters
    ----------
    hours_1 : int
        number between 0 and 23.
    mins_1 : int
        number between 0 and 59.
    hours_2 : int
        number between 0 and 23.
    mins_2 : int
        number between 0 and 59.

    Returns
    -------
    diff_hours : int
        difference in hours.
    diff_mins : TYPE
        difference in minutes

    """
    
    # difference between both hours
    if hours_1 >= hours_2:
        diff_hours = hours_1 - hours_2
        # difference between both minutes
        diff_hours, diff_mins = get_calc_mins(diff_hours, mins_1, mins_2)
        
    else:
        diff_hours = hours_2 - hours_1
        # difference between both minutes
        diff_hours, diff_mins = get_calc_mins(diff_hours, mins_2, mins_1)
        # print(diff_hours, diff_mins)
    return diff_hours, diff_mins


def calc_sum(time_1, time_2):
    """
    Calculates the sum of two times

    Parameters
    ----------
    time_1 : string
        time in the format hh:mm.
    time_2 : string 
        time in the format hh:mm

    Returns
    -------
    str
        time in the format hh:mm

    """
    hours_1, mins_1 = split_time(time_1)
    hours_2, mins_2 = split_time(time_2)
    
    sum_mins = mins_1 + mins_2
    sum_hours = hours_1 + hours_2
    if sum_mins > 59:
        sum_mins -= 60
        sum_hours += 1
    return f'{formate_clock(sum_hours)}:{formate_clock(sum_mins)}'
        

def get_time_sum(time_list):
    """
    calculates the sum of a list of time strings

    Parameters
    ----------
    time_list : list of strings with format "hh:mm"
        list with strings with different times which should be summed up

    Returns
    -------
    time_sum : list of strings with format "hh:mm"
        sum of all times.

    """
    # print(time_list)
    if isinstance(time_list, list) and len(time_list) > 1:
        # print(time_list)
        for idx in range(1, len(time_list)):
            if idx == 1:
                time_sum = calc_sum(time_list[0], time_list[idx])
            else:
                time_sum = calc_sum(time_sum, time_list[idx])
        return time_sum
    elif len(time_list) == 1:
        return time_list[0]
    elif len(time_list) == 0:
        # when the list has no entry -> return the time "0:00" -> expects a value
        return "0:00"
    else:
        return time_list

        
def split_time(time):
    """
    splits the string time into two integer and returns

    Parameters
    ----------
    time : string
        time

    Returns
    -------
    hours : int
        returns hours
    mins : int
        returns mins

    """
    # print(time)
    try:
        if isinstance(time, str):
            time_str = time.split(':')
            hours = int(time_str[0])
            mins = int(time_str[1])
            return hours, mins
        else:
            return time
    except ValueError:
        print(time)
        return time

def get_time_dif(time_1, time_2, rv='all'):
    """
        needs to times to be evaluated and calculates the difference between 
        both times and returns the difference in minutes and hours in the
        format hh:mm

    Parameters
    ----------
    time_1 : String - hh:mm
        time 1 which is to be compared.
    time_2 : String or list, with following representation- hh:mm
        time 2 which is to be compared.

    Returns 
    -------
    time difference as string in representation "hh:mm"

    """
    if isinstance(time_1, list):    
        # print(time_1)
        hours_1, mins_1 = split_time(get_time_sum(time_1))
    else:
        hours_1, mins_1 = split_time(time_1)
    
    if isinstance(time_2, list):    
        # print(time_1)
        hours_2, mins_2 = split_time(get_time_sum(time_2))
    else:
        hours_2, mins_2 = split_time(time_2)
    

    # print(hours_2, mins_2, hours_1, mins_1)
    diff_hours, diff_mins = get_calc_dif(hours_1, mins_1, hours_2, mins_2)
    
    if rv=='all':
        return f"{formate_clock(diff_hours)}:{formate_clock(diff_mins)}"
    elif rv=='mins':
        return str(60*diff_hours+diff_mins)
    
    
if __name__ == '__main__':
    arbeitswoche = ""    
    today_start = ""
    week = []
    
    print(f"Uhrzeit: {datetime.datetime.now().strftime('%H:%M')} Uhr\n")
    
    left_arbeitswoche = get_time_dif(arbeitswoche, get_time_sum(week))
    cur_work = get_work_hour(today_start)
    week.append(cur_work)
    
    week_work = get_time_sum(week)
    time_left = get_time_dif(arbeitswoche, week_work)
    daily_work = get_daily_work_hour(left_arbeitswoche, workdays=5-len(week)+1)
    
    print(f'heutige Pausenzeit: {get_time_pause(today_start)} h')
    print(f'heutige Arbeitszeit: {cur_work} h')
    print(f'tägliche Arbeitszeit: {daily_work} h')
    print(f'wöchentliche Arbeitszeit: {week_work} h')
    print(f'restliche Arbeitszeit: {time_left} h')
    print(f'Ende Arbeitszeit: {get_end_work(cur_work, daily_work)} Uhr')
