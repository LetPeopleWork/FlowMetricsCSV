from WorkItem import WorkItem
from datetime import datetime

import csv

class CsvService:    
       
    def parse_items(self, file_path, delimeter, started_date_column_name, closed_date_column_name, date_format):
        print("Loading Items from CSV File: '{0}'. Started Date Column Name '{1}', Closed Date Column Name '{2} and Date Format '{3}'".format(file_path, closed_date_column_name, started_date_column_name, date_format))
        work_items = []
        
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=delimeter)
            
            for row in csv_reader:
                closed_date = row[closed_date_column_name]
                if closed_date:
                    closed_date = datetime.strptime(closed_date, date_format)      

                started_date = row[started_date_column_name]
                if started_date:    
                    started_date = datetime.strptime(started_date, date_format)        
                       
                work_items.append(WorkItem(started_date, closed_date))
        
        print("Found {0} Items in the CSV".format(len(work_items)))

        return work_items
