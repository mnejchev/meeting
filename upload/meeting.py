import numpy as np


def get_available_time(schedule, worktime, meeting_duration):

    schedule = free_time(convert_to_minutes(schedule), convert_to_minutes(worktime))
    schedule = filtering(schedule, meeting_duration)

    return schedule


def convert_to_minutes(schedule: list):

    dimensions = np.array(schedule).ndim

    if dimensions == 2:
        for window in schedule:
            for clock in window:

                hours, minutes = clock.split(":")

                hours = int(hours)
                minutes = int(minutes) + (hours * 60)
                schedule[schedule.index(window)][window.index(clock)] = minutes
    else:
        for clock in schedule:
            hours, minutes = clock.split(":")

            hours = int(hours)
            minutes = int(minutes) + (hours * 60)
            schedule[schedule.index(clock)] = minutes

    return schedule


def free_time(schedule: list, worktime_in_minutes: list):

    free_time_schedule = [[worktime_in_minutes[0], schedule[0][0]]]

    for x in range(len(schedule) - 1):

        current_pair = []
        time_index = 1
        window_index = 0

        for i in range(2):
            current_pair.append(schedule[x + window_index][time_index])
            time_index = 0
            window_index = 1

        free_time_schedule.append(current_pair)

    free_time_schedule.append([schedule[-1][-1], worktime_in_minutes[-1]])

    return free_time_schedule


def filtering(free_schedule: list, time: int):

    free_schedule = list(filter(lambda x: x[1] - x[0] >= time, free_schedule))

    return free_schedule


def minutes_to_hours(schedule):

    for a in schedule:
        index_a = schedule.index(a)

        for b in a:
            index_b = schedule[schedule.index(a)].index(b)

            hours = str(b // 60)
            if len(hours) == 1:
                hours += 0

            minutes = str(b % 60)
            if len(minutes) == 1:
                minutes += "0"

            schedule[index_a][index_b] = f"{hours}:{minutes}"

        schedule[index_a] = " - ".join(schedule[index_a])

    return schedule


person_one_schedule = [x.split(" - ") for x in input().split(", ")]
person_one_worktime = input().split(" - ")

person_two_schedule = [x.split(" - ") for x in input().split(", ")]
person_two_worktime = input().split(" - ")

print(f"Person #1:\nSchedule:{person_one_schedule}\nWorktime: {person_one_worktime}")
print(f"Person #2:\n{person_two_schedule}\nWorktime: {person_two_worktime}")

meeting_time = 30  # minutes

first_available = get_available_time(person_one_schedule, person_one_worktime, meeting_time)
second_available = get_available_time(person_two_schedule, person_two_worktime, meeting_time)

matching = []
for first_person_period in first_available:  # appending matches

    start, end = first_person_period[0], first_person_period[1]

    for second_person_period in second_available:
        start_2, end_2 = second_person_period[0], second_person_period[1]

        if start_2 in range(start, end):

            if end_2 in range(start, end):
                matching.append(second_person_period)
            else:
                matching.append([start_2, end])

        elif end_2 in range(start, end):

            matching.append([start, end_2])

        elif start in range(start_2, end_2) and end in range(start_2, end_2):
            matching.append(first_person_period)

matching = filtering(matching, meeting_time)
matching = minutes_to_hours(matching)

for z in range(len(matching)):
    print(f"\nPossible meeting № {z}: {matching[z]}")
