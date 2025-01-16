from datetime import datetime, timedelta

def is_valid_datetime(user_input, timedlt: list, date_format="%d.%m.%Y %H:%M"):
    try:
        end_datetime = datetime.strptime(user_input, date_format)

        if timedlt[0] == "1":
            end_datetime -= timedelta(hours=int(timedlt[1]), minutes=int(timedlt[2]))
        elif timedlt[0] == "-1":
            end_datetime += timedelta(hours=int(timedlt[1]), minutes=int(timedlt[2]))

        # return end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # if end_datetime >= datetime.now() + timedelta(minutes=60):
        if end_datetime >= datetime.now():
            return end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None
    except ValueError:
        return None


def get_time_difference(user_input, date_format="%d.%m.%Y %H:%M"):
    try:
        user_time = datetime.strptime(user_input, date_format)
        now = datetime.now()
        if user_time > now:
            tsign = 1
            time_diff = user_time - now
        elif user_time < now:
            tsign = -1
            time_diff = now - user_time
        else:
            tsign = 0
            time_diff = 0
    
        return f"{tsign}:{time_diff.seconds // 3600}:{(time_diff.seconds % 3600) // 60}"
    
    except ValueError:
        return None