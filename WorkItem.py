from datetime import datetime

class WorkItem:
    def __init__(self, started_date, closed_date):
        self.started_date = started_date
        self.closed_date = None

        self.work_item_age = None
        self.cycle_time = None

        if closed_date:
            self.closed_date = closed_date
            self.cycle_time = (closed_date - started_date).days + 1
        else:
            self.work_item_age = (datetime.today() - started_date).days + 1
            
    def to_dict(self):
            return {
                'started_date': self.started_date.date(),
                'closed_date': self.closed_date.date(),
                'work_item_age': self.work_item_age,
                'cycle_time': self.cycle_time,
            }