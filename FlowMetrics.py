import argparse

from datetime import datetime
from CsvService import CsvService
from FlowMetricsService import FlowMetricsService

import json

parser = argparse.ArgumentParser()
parser.add_argument("--ConfigFileNames", type=str, nargs='+', default=["config.json"])

args = parser.parse_args()

def read_config(file_path):
    print("Reading Config File from {0}".format(file_path))
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

config_paths = args.ConfigFileNames
print("Using following configuration files: {0}".format(config_paths))

for config_path in config_paths:
    print("================================================================")
    config = read_config(config_path)

    file_name = config["general"]["fileName"]
    deliemter = config["general"]["delimeter"]
    started_date_column = config["general"]["startedDateColumn"]
    closed_date_column = config["general"]["closedDateColumn"]
    start_date_format = config["general"]["startDateFormat"]
    closed_date_format = config["general"]["closedDateFormat"]
    estimation_column = config["general"]["estimationColumn"]
    item_title_column = config["general"]["itemTitleColumn"]
    show_plots = config["general"]["showPlots"]
    charts_folder = config["general"]["chartsFolder"]

    if not closed_date_format:
        closed_date_format = start_date_format

    csv_service = CsvService()
    flow_metrics_service = FlowMetricsService(show_plots, charts_folder)

    def get_items():    
        work_items = csv_service.parse_items(file_name, deliemter, started_date_column, closed_date_column, start_date_format, closed_date_format, estimation_column, item_title_column)
        return work_items

    
    print("Creating Charts as per the configuration...")
    print("----------------------------------------------------------------")   


    work_items = get_items()        
    if len(work_items) < 1:
        print("No items - skipping")
        exit()

    def create_cycle_time_scatterplot():
        chart_config = config["cycleTimeScatterPlot"]

        if chart_config["generate"]:
            flow_metrics_service.plot_cycle_time_scatterplot(work_items, chart_config["history"], chart_config["percentiles"], chart_config["percentileColors"], chart_config["chartName"])

    def create_work_item_age_scatterplot():
        chart_config = config["workItemAgeScatterPlot"]

        if chart_config["generate"]:
            flow_metrics_service.plot_work_item_age_scatterplot(work_items, chart_config["history"], chart_config["xAxisLines"], chart_config["xAxisLineColors"], chart_config["chartName"])

    def create_throughput_run_chart():
        chart_config = config["throughputRunChart"]

        if chart_config["generate"]:
            flow_metrics_service.plot_throughput_run_chart(work_items, chart_config["history"], chart_config["chartName"], chart_config["unit"])

    def create_work_in_process_run_chart():
        chart_config = config["workInProcessRunChart"]

        if chart_config["generate"]:
            flow_metrics_service.plot_work_in_process_run_chart(work_items, chart_config["history"], chart_config["chartName"])

    def create_work_started_vs_finished_chart():
        chart_config = config["startedVsFinishedChart"]

        if chart_config["generate"]:
            flow_metrics_service.plot_work_started_vs_finished_chart(work_items, chart_config["history"], chart_config["startedColor"], chart_config["closedColor"], chart_config["chartName"])

    def create_estimation_vs_cycle_time_chart():
        chart_config = config["estimationVsCycleTime"]

        if chart_config["generate"]:
            flow_metrics_service.plot_estimation_vs_cycle_time_scatterplot(work_items, chart_config["history"], chart_config["chartName"], chart_config["estimationUnit"])
    
    def create_process_behaviour_charts():
        chart_config = config["processBehaviourCharts"]

        if chart_config["generate"]:
            history = chart_config["history"]
            baseline_start = datetime.strptime(chart_config["baselineStart"], "%Y-%m-%d")
            baseline_end = datetime.strptime(chart_config["baselineEnd"], "%Y-%m-%d")
            
            flow_metrics_service.plot_throughput_process_behaviour_chart(work_items, baseline_start, baseline_end, history, chart_config["throughputChartName"])

    create_cycle_time_scatterplot()
    create_work_item_age_scatterplot()
    create_throughput_run_chart()
    create_work_in_process_run_chart()
    create_work_started_vs_finished_chart()
    create_estimation_vs_cycle_time_chart()    
    create_process_behaviour_charts()