from ortools.sat.python import cp_model

import pandas as pd
# Create the model.
model = cp_model.CpModel()

# Create variables.
num_teachers = 15
num_classes = 8
num_days = 5  # Five days in a working week
num_periods_per_day = 6  # Varying periods on different days
classes = range(num_classes)
days = range(num_days)
teachers = range(num_teachers)
periods = range(num_periods_per_day)

days_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
periods_dict = {0: '1st', 1: '2nd', 2: '3rd', 3: '4th', 4: '5th', 5: '6th'}
teachers_dict= {0: 'Mr. A', 1: 'Mr. B', 2: 'Mr. C', 3: 'Mr. D', 4: 'Mr. E', 5: 'Mr. F', 6: 'Mr. G', 7: 'Mr. H', 8: 'Mr. I', 9: 'Mr. J', 10: 'Mr. K', 11: 'Mr. L', 12: 'Mr. M', 13: 'Mr. N', 14: 'Mr. O'}

# The periods per day are varying, so we need to manage them accordingly
# periods = {}
# for i in range(num_days):
#     periods[i] = range(num_periods_per_day[i])

# Create schedule variables.
x = {}
for teacher in teachers:
    for day in days:
        for period in periods:
            for cls in classes:
                x[teacher, day, period, cls] = model.NewBoolVar('schedule_%i%i%i%i' % (teacher, day, period, cls))

# For the teaching schedules, I'm assuming that each teacher can teach each class twice a week.
# Also, the dict values should now be in lists since we have more than one day with the same number of periods.
teaching_schedules = {
    0: {0: 4, 1: 4, 2: 4, 3: 4, 4: 4},
    1: {5: 4, 6: 4, 7: 4},
    2: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    3: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    4: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    5: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    6: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    7: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    8: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    9: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    10: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    11: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    12: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    13: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    14: {0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
}




# not available teachers
teacher_unavailability = {
    9: [(0,0)],  # Teacher 0 is unavailable on Day 0 Period 0
    3: [(0,0)],
    1: [(0,0),(1,0),(2,0),(3,0),(4,0)],
    0: [(0,0)],
}

# Create schedule variables.
x = {}
for teacher in teachers:
    for day in days:
        for period in periods:
            for cls in classes:
                # If the teacher is unavailable at this day and period, don't create a variable
                if (day, period) in teacher_unavailability.get(teacher, []):
                    continue
                x[teacher, day, period, cls] = model.NewBoolVar('schedule_%i%i%i%i' % (teacher, day, period, cls))



# Constraint: Each teacher can teach at most one class per period.
for teacher in teachers:
    for day in days:
        for period in periods:
            model.Add(sum(x.get((teacher, day, period, cls), 0) for cls in classes) <= 1)

# Constraint: Only one teacher can teach a class at a specific day and period.
for cls in classes:
    for day in days:
        for period in periods:
            model.Add(sum(x.get((teacher, day, period, cls), 0) for teacher in teachers) <= 1)

# Constraint: Teacher cannot teach the same class more than once per day.
for teacher in teachers:
    for cls in classes:
        for day in days:
            model.Add(sum(x.get((teacher, day, period, cls), 0) for period in periods) <= 1)


# Constraint: If a teacher teaches two periods consecutively, they can't teach in the next period.
for teacher in teachers:
    for day in days:
        for period in range(num_periods_per_day - 2):  # Adjusted range
            model.Add(sum(x.get((teacher, day, p, cls), 0) for p in range(period, period + 3) for cls in classes) <= 2)




# Constraint: Each teacher has a certain number of lectures to teach per week for each class.
for teacher, schedule in teaching_schedules.items():
    for cls, num_lectures in schedule.items():
        model.Add(sum(x.get((teacher, day, period, cls), 0) for day in days for period in periods) == num_lectures)

# Create the solver and solve.
solver = cp_model.CpSolver()
status = solver.Solve(model)

# timetable for each class
if status == cp_model.OPTIMAL:
    schedule_matrices = [[[None for _ in days] for _ in periods] for _ in classes]

    for cls in classes:
        for day in days:
            for period in periods:
                for teacher in teachers:
                    if solver.Value(x.get((teacher, day, period, cls), 0)):
                        schedule_matrices[cls][period][day] = teachers_dict[teacher]

    # Convert schedule_matrices to pandas DataFrame
    dfs_by_class = []
    for cls, timetable_matrix in enumerate(schedule_matrices):
        df_by_class = pd.DataFrame(
            timetable_matrix,
            columns=[f"{days_dict[day]}" for day in days],
            index=[f"{periods_dict[period]}" for period in periods],
        )
        dfs_by_class.append((cls, df_by_class))

    # Print the timetable for each teacher
    for cls, df_by_class in dfs_by_class:
        print(f"class : {cls}'s Timetable:")
        print(df_by_class)
        print()






if status == cp_model.OPTIMAL:
    # Create empty schedule matrices for each teacher
    schedule_matrices = [[[None for _ in days] for _ in periods] for _ in teachers]

    for teacher in teachers:
        for day in days:
            for period in periods:
                for cls in classes:
                    if solver.Value(x.get((teacher, day, period, cls), 0)):
                        schedule_matrices[teacher][period][day] = cls

    # Convert schedule_matrices to pandas DataFrame
    dfs_by_teacher = []
    for teacher, timetable_matrix in enumerate(schedule_matrices):
        df_by_teacher = pd.DataFrame(
            timetable_matrix,
            columns=[f"{days_dict[day]}" for day in days],
            index=[f"{periods_dict[period]}" for period in periods],
        )
        dfs_by_teacher.append((teacher, df_by_teacher))

    # Print the timetable for each teacher
    for teacher, df_by_teacher in dfs_by_teacher:
        print(f"Teacher {teachers_dict[teacher]}'s Timetable:")
        print(df_by_teacher)
        print()

print('Solve status: %s' % solver.StatusName(status))


#calculate how long it takes to run the program





