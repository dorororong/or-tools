# if status == cp_model.OPTIMAL:
#     # Create empty schedule matrices for each teacher
#     schedule_matrices = [[[None for _ in days] for _ in periods] for _ in teachers]
#
#     for teacher in teachers:
#         for day in days:
#             for period in periods:
#                 for cls in classes:
#                     if solver.Value(x.get((teacher, day, period, cls), 0)):
#                         schedule_matrices[teacher][period][day] = cls
#
#     # Convert schedule_matrices to pandas DataFrame
#     dfs_by_teacher = []
#     for teacher, timetable_matrix in enumerate(schedule_matrices):
#         df_by_teacher = pd.DataFrame(
#             timetable_matrix,
#             columns=[f"{days_dict[day]}" for day in days],
#             index=[f"{periods_dict[period]}" for period in periods],
#         )
#         dfs_by_teacher.append((teacher, df_by_teacher))
#
#     # Print the timetable for each teacher
#     for teacher, df_by_teacher in dfs_by_teacher:
#         print(f"Teacher {teachers_dict[teacher]}'s Timetable:")
#         print(df_by_teacher)
#         print()