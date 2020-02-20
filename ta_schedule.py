from __future__ import print_function
from ortools.sat.python import cp_model


# all TAs work_hours must be 6

def main():
    num_tas = 2
    num_hours = 3
    num_days = 4

    all_tas = range(num_tas)
    all_hours = range(num_hours)
    all_days = range(num_days)

    hour_pref = [[[0, 1, 0], [1, 1, 0], [1, 0, 1], [1, 0, 0]],
                 [[1, 1, 1], [0, 0, 0], [0, 0, 1], [1, 0, 0]]]

    model = cp_model.CpModel()

    shifts = {}
    for t in all_tas:
        for d in all_days:
            for s in all_hours:
                shifts[(t, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (t, d, s))

    min_shifts_per_tas = 3
    max_shifts_per_tas = 3

    for t in all_tas:
        num_shifts_worked = sum(
            shifts[(t, d, s)] for d in all_days for s in all_hours)
        model.Add(min_shifts_per_tas <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_tas)

    model.Add(
hour_pref[n][d][s] * shifts[(n, d, s)] for n in all_tas
            for d in all_days for s in all_hours))

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for t in all_tas:
            for s in all_hours:
                if solver.Value(shifts[(t, d, s)]) == 1:
                    if hour_pref[t][d][s] == 1:
                        print('Ta', t, 'works shift', s, '(requested).')
                    else:
                        print('Ta', t, 'works shift', s, '(not requested).')
        print()

    # Statistics.
    print()
    print('Statistics')
    print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
          '(out of', num_tas * min_shifts_per_tas, ')')
    print('  - wall time       : %f s' % solver.WallTime())


if __name__ == '__main__':
    main()
