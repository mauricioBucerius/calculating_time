# calculating_time
to work with time as a string. Adding or subtracting times as a string. The times are formated in "hh:mm", for example "12:34". In case of a single digit like "08:04", the "0" in front of the digit is optional. But the output of the function is always with a "0" in front of the digits.

## 📐 How-To
### Adding
The function *get_time_sum()* takes a list as input and adds them together. The list contains multiple times.
- `get_time_sum(["8:08", "7:15"]) -> "15:23"`

### Subtracting
The function *get_time_dif()* calculates the difference between two inputs. Which one the two inputs is the larger one doesn't matter at all. You can commit a list instead of a single time. But In case of a list the list will summed up and calculates afterwards the difference between the sum of the list and the other input:
- `get_time_dif(["8:02", "5:00"], ["6:02", "1:00"]) -> "06:00"`
- `get_time_dif("8:02", ["6:02", "1:00"]) -> "01:00"`
- `get_time_dif("8:02", "6:02") -> "02:00"`

#### ⚡️ Warning:
A negative difference is in the implemented way not possible, because it always calculates the larger minus the smaller time!

### Work Hour
Calculates the current workhour and subtracts the time with pause. The input expects a time, where you started with work. The function checks the system time and formates them to "hh:mm"
- `get_work_hour("8:00") -> "4:30"` 
