from datetime import timedelta, datetime


def create_pill_schedule(periodicity: int):
    start, finish = timedelta(hours=8), timedelta(hours=22)
    if periodicity == 1:
        return (start,)
    general_interval = finish - start
    step_interval: int = int((general_interval.seconds / (periodicity - 1)))  # from 8 to 22, 15 tablets
    range_pill_schedule = range(start.seconds, finish.seconds + 5, step_interval)
    return (timedelta(seconds=round_time(time)) for time in range_pill_schedule)


def round_time(time: int) -> int:
    if time // 60 % 15 == 0:
        return time
    time -= time % 60
    return time - time % (15 * 60) + 15 * 60


def get_time_next_pills(periodicity: int) -> None | list[str]:
    near_future = timedelta(hours=1, minutes=0)  # config service
    pill_schedule = create_pill_schedule(periodicity)
    current_time = datetime.now().time()
    current_time = timedelta(hours=current_time.hour, minutes=current_time.minute)
    if current_time > timedelta(hours=22) and near_future > timedelta(hours=10):
        return None
    time_next_pills: list[str] = []
    for time_pill in pill_schedule:
        if time_pill < current_time:
            continue
        elif time_pill > current_time:
            if time_pill - current_time <= near_future:
                time_next_pills.append(str(time_pill))
            else:
                break
    return time_next_pills
