from .WorkItem import WorkItem
from datetime import datetime, timedelta

import random

import csv

class CsvService:    
       
    def parse_items(self, file_path, delimeter, started_date_column_name, closed_date_column_name, start_date_format, closed_date_format, estimation_column_name, item_title_column):
        print("Loading Items from CSV File: '{0}'. Started Date Column Name '{1}', Closed Date Column Name '{2}', Start Date Format '{3}', and Closed Date Format '{4}'".format(file_path, started_date_column_name, closed_date_column_name, start_date_format, closed_date_format))
        work_items = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as file:
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

    def write_example_file(self, file_path, delimeter, started_date_column_name, closed_date_column_name, start_date_format, closed_date_format, estimation_column_name, item_title_column):
        print("Writing Example File with random values to {0}".format(file_path))
        
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=delimeter)
            field = [started_date_column_name, closed_date_column_name, estimation_column_name, item_title_column]
            
            # Write Header
            writer.writerow(field)
            
            story_points = [1, 2, 3, 5, 8, 13]
            
            # Generate and write 100 random dates
            for index in range(100):
                start_date_delta = random.randint(0, 30)
                
                random.seed()
                
                end_date_delta = random.randint(0, 30)
                
                random_start_date = datetime.now() - timedelta(days=start_date_delta)
                random_end_date = datetime.now() - timedelta(days=end_date_delta)
                
                started_date = random_start_date.strftime(start_date_format)
                end_date = ""
                
                if end_date_delta <= start_date_delta:
                    end_date = random_end_date.strftime(closed_date_format)
                
                estimation = random.choice(story_points)
                
                writer.writerow([started_date, end_date, estimation, index])