from .WorkItem import WorkItem
from datetime import datetime

import csv

class CsvService:    
       
    def parse_items(self, file_path, delimeter, started_date_column_name, closed_date_column_name, start_date_format, closed_date_format, estimation_column_name, item_title_column):
        print("Loading Items from CSV File: '{0}'. Started Date Column Name '{1}', Closed Date Column Name '{2}', Start Date Format '{3}', and Closed Date Format '{4}'".format(file_path, started_date_column_name, closed_date_column_name, start_date_format, closed_date_format))
        work_items = []
        
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=delimeter)
            
            for row in csv_reader:
                closed_date = row[closed_date_column_name]
                if closed_date:
                    closed_date = datetime.strptime(closed_date, closed_date_format)      

                started_date = row[started_date_column_name]
                if started_date:    
                    started_date = datetime.strptime(started_date, start_date_format)        

                estimation = None
                if estimation_column_name in row:
                    raw_estimate = row[estimation_column_name]
                    estimation = 0

                    if raw_estimate:
                        estimation = float(row[estimation_column_name])
                    
                item_title = ""
                if item_title_column in row:
                    item_title = row[item_title_column]
                       
                work_items.append(WorkItem(started_date, closed_date, item_title, estimation))
        
        print("Found {0} Items in the CSV".format(len(work_items)))

        return work_items
