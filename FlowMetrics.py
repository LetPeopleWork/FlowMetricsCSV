import argparse

from CsvService import CsvService
from FlowMetricsService import FlowMetricsService

parser = argparse.ArgumentParser()
parser.add_argument("--FileName", default=".\\ExampleFile.csv")
parser.add_argument("--Delimeter", default=";")
parser.add_argument("--StartedDateColumn", default="Activated Date")
parser.add_argument("--ClosedDateColumn", default="Closed Date")
parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
parser.add_argument("--History", default="90")
parser.add_argument("--ShowPlots", default=False, action=argparse.BooleanOptionalAction)

args = parser.parse_args()

file_name = args.FileName
deliemter = args.Delimeter
started_date_column = args.StartedDateColumn
closed_date_column = args.ClosedDateColumn
date_format = args.DateFormat
history = int(args.History)
show_plots = args.ShowPlots

csv_service = CsvService()
flow_metrics_service = FlowMetricsService()

def get_items():    
    work_items = csv_service.parse_items(file_name, deliemter, started_date_column, closed_date_column, date_format)
    return work_items

print("================================================================")
print("Calculating Flow Metrics...")
print("================================================================")  
print("Parameters:")
print("FileName: {0}".format(file_name))
print("Delimeter: {0}".format(deliemter))
print("Start Date Column: {0}".format(started_date_column))
print("Closed Date Column: {0}".format(closed_date_column))
print("DateFormat: {0}".format(date_format))
print("History: {0}".format(history))
print("Show Plots: {0}".format(show_plots))
print("----------------------------------------------------------------")   


work_items = get_items()        
if len(work_items) < 1:
    print("No items - skipping")
    exit()

flow_metrics_service.plot_cycle_time_scatterplot(work_items, history, show_plots)
flow_metrics_service.plot_work_item_age_scatterplot(work_items, history, show_plots)
flow_metrics_service.plot_throughput_run_chart(work_items, history, show_plots)
flow_metrics_service.plot_work_in_process_run_chart(work_items, history, show_plots)
