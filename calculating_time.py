import datetime
import numpy as np
    
TIME_BREAKFAST = "9:30"     # breakfast time in the morning
TIME_LUNCH = "11:30"        # lunch time in the midday

DURATION_BREAKFAST = "0:15" # Breakfast break 
DURATION_LUNCH = "0:30"     # Lunch break

def get_daily_work_hour(worktime, workdays=5):
    hours, mins = split_time(worktime)
    hours_daily = int(np.floor(hours/workdays))
    mins_daily = round(mins/workdays + (hours/workdays - hours_daily)*60)
    return f'{formate_clock(hours_daily)}:{formate_clock(mins_daily)}'

def get_work_hour(start, **kwargs):
    time_now = datetime.datetime.now().strftime("%H:%M")
    breakfast = False
    lunch = False
    lunch_pause = "0:00"
                
    if not is_later(start, TIME_BREAKFAST) and is_later(time_now, TIME_BREAKFAST):
        breakfast = True

    if not is_later(start, TIME_LUNCH) and is_later(time_now, TIME_LUNCH):
        lunch = True
        
    for key, value in kwargs.items():
        if key == 'lunch_pause':
            lunch_pause = value
            lunch = False
            
    if lunch and breakfast:
        time_pause = "0:45"
    elif lunch:
        time_pause = "0:30"
    elif breakfast:
        time_pause = "0:15"
    else:
        time_pause = "0:00"
        
    time_pause = get_time_sum([time_pause, lunch_pause])
    print(f'heutige Pausenzeit: {time_pause} h')
    return get_time_dif(time_now, [start, time_pause])

def get_end_work(current_worktime, worktime):
    time_now = datetime.datetime.now().strftime("%H:%M")
    time_left = get_time_dif(worktime, current_worktime)
    return get_time_sum([time_now, time_left])


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
        
    
def is_later(time_1, comp_time):
    hours_1, mins_1 = split_time(time_1)
    hours_2, mins_2 = split_time(comp_time)
    
    # print(mins_1, mins_2)
    # compares if time_1 is before time_2 or later
    if hours_1 < hours_2:
        return False
    
    if hours_1 == hours_2 and mins_1 < mins_2:
        return False
    
    return True
    
def get_calc_dif(hours_1, mins_1, hours_2, mins_2):
    # difference between both hours
    if hours_1 >= hours_2:
        diff_hours = hours_1 - hours_2
        
        # difference between both minutes
        if mins_1 > mins_2:
            diff_mins = mins_1 - mins_2
        else:
            # if mins_1 smaller, then there is no full hour between both
            # times and you have to calc the difference between mins_1 to the 
            # full 60 minutes and the add the mins_1 for the real difference
            mins_to_60 = 60 - mins_2
            diff_mins = mins_1 + mins_to_60
            
            if diff_mins == 60:
                # If the difference is 60 - zero it and don't subtract the hours
                diff_mins = 0 
            else:    
                diff_hours -= 1     # there is no full hour difference -> sub 1
    else:
        diff_hours = hours_2 - hours_1
        # difference between both minutes
        if mins_2 > mins_1:
            diff_mins = mins_2 - mins_1
        else:
            # if mins_1 smaller, then there is no full hour between both
            # times and you have to calc the difference between mins_1 to the 
            # full 60 minutes and the add the mins_1 for the real difference
            mins_to_60 = 60 - mins_2
            diff_mins = mins_1 + mins_to_60
            
            if diff_mins == 60:
                # If the difference is 60 - zero it and don't subtract the hours
                diff_mins = 0 
            else:    
                diff_hours -= 1     # there is no full hour difference -> sub 1
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
    if isinstance(time, str):
        time_str = time.split(':')
        hours = int(time_str[0])
        mins = int(time_str[1])
        return hours, mins
    else:
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
    arbeitswoche = "38:00"    
    today_start = "8:19"
    week = []
    left_arbeitswoche = get_time_dif(arbeitswoche, get_time_sum(week))
    cur_work = get_work_hour(today_start)
    week.append(cur_work)
    
    week_work = get_time_sum(week)
    time_left = get_time_dif(arbeitswoche, week_work)
    daily_work = get_daily_work_hour(left_arbeitswoche, workdays=5-len(week)+1)
    
    print(f'tägliche Arbeitszeit: {daily_work} h')
    print(f'heutige Arbeitszeit: {cur_work} h')
    print(f'wöchentliche Arbeitszeit: {week_work} h')
    print(f'restliche Arbeitszeit: {time_left} h')
    print(f'Ende Arbeitszeit: {get_end_work(cur_work, daily_work)} Uhr')