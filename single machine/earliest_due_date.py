def earliest_due_date(due_dates):
    return sorted(range(len(due_dates)), key=lambda i: due_dates[i])
