from scheptk.scheptk import SingleMachine
from earliest_due_date import earliest_due_date

instance = SingleMachine('test_single.txt')

due_dates = instance.dd

solution = earliest_due_date(due_dates)

print('Total tardiness is {}'.format(instance.SumTj(solution)))
print('Sequence: ', solution)
instance.print_schedule(solution, 'gantt_single.png')


