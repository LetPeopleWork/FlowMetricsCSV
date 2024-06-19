import argparse
import os
import shutil
from datetime import datetime
from .CsvService import CsvService
from .FlowMetricsService import FlowMetricsService
import json

def print_logo():
    logo = r"""
    /$$                 /$$           /$$$$$$$                           /$$                /$$      /$$                  /$$      
    | $$                | $$          | $$__  $$                         | $$               | $$  /$ | $$                 | $$      
    | $$       /$$$$$$ /$$$$$$        | $$  \ $$/$$$$$$  /$$$$$$  /$$$$$$| $$ /$$$$$$       | $$ /$$$| $$ /$$$$$$  /$$$$$$| $$   /$$
    | $$      /$$__  $|_  $$_/        | $$$$$$$/$$__  $$/$$__  $$/$$__  $| $$/$$__  $$      | $$/$$ $$ $$/$$__  $$/$$__  $| $$  /$$/
    | $$     | $$$$$$$$ | $$          | $$____| $$$$$$$| $$  \ $| $$  \ $| $| $$$$$$$$      | $$$$_  $$$| $$  \ $| $$  \__| $$$$$$/ 
    | $$     | $$_____/ | $$ /$$      | $$    | $$_____| $$  | $| $$  | $| $| $$_____/      | $$$/ \  $$| $$  | $| $$     | $$_  $$ 
    | $$$$$$$|  $$$$$$$ |  $$$$/      | $$    |  $$$$$$|  $$$$$$| $$$$$$$| $|  $$$$$$$      | $$/   \  $|  $$$$$$| $$     | $$ \  $$
    |________/\_______/  \___/        |__/     \_______/\______/| $$____/|__/\_______/      |__/     \__/\______/|__/     |__/  \__/
                                                        | $$                                                                
                                                        | $$                                                                
                                                        |__/                                                                
    """
    print(logo)

def copy_default_config(script_dir):        
    default_config_file = os.path.join(script_dir, "ExampleConfig.json")
    
    config_file_destination = os.path.join(os.getcwd(), os.path.basename(default_config_file))        
    if not check_if_file_exists(config_file_destination):
        shutil.copy(default_config_file, config_file_destination)

def check_if_file_exists(file_path, raise_if_not_found = False):
    if not os.path.isfile(file_path):
        if raise_if_not_found:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
        return False
    
    return True

def read_config(file_path):
    print("Reading Config File from {0}".format(file_path))
    
    check_if_file_exists(file_path, True)
    
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data
    
def main():
    try:
        print_logo()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--ConfigFileNames", type=str, nargs='+', default=[])

        args = parser.parse_args()
        
        config_paths = args.ConfigFileNames
        
        using_example_config = False
        if len(config_paths) < 1:
            print("No config file specified, copying defaults and using them")
            copy_default_config(script_dir)
            config_paths.append("ExampleConfig.json")
            using_example_config = True
        
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
            
            print("Using following CSV file: {0}".format(file_name))
            file_exists = check_if_file_exists(file_name, not using_example_config)                
            
            if using_example_config and not file_exists:
                csv_service.write_example_file(file_name, deliemter, started_date_column, closed_date_column, start_date_format, closed_date_format, estimation_column, item_title_column)

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
                
                trend_settings = None
                if "trend_settings" in chart_config:
                    trend_settings = chart_config["trend_settings"]

                if chart_config["generate"]:
                    flow_metrics_service.plot_cycle_time_scatterplot(work_items, chart_config["history"], chart_config["percentiles"], chart_config["percentileColors"], chart_config["chartName"], trend_settings)

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
                    flow_metrics_service.plot_wip_process_behaviour_chart(work_items, baseline_start, baseline_end, history, chart_config["wipChartName"])
                    flow_metrics_service.plot_cycle_time_process_behaviour_chart(work_items, baseline_start, baseline_end, history, chart_config["cycleTimeChartName"])       
                    flow_metrics_service.plot_total_age_process_behaviour_chart(work_items, baseline_start, baseline_end, history, chart_config["itemAgeChartName"])                        

            create_cycle_time_scatterplot()
            create_work_item_age_scatterplot()
            create_throughput_run_chart()
            create_work_in_process_run_chart()
            create_work_started_vs_finished_chart()
            create_estimation_vs_cycle_time_chart()    
            create_process_behaviour_charts()       

            print()
            print()
            print()
            print("🛈 Want to learn more about how all of this works? Check out out website! 🛈")
            print("🔗 https://letpeople.work 🔗")
    except Exception as exception:
        print("Error while executing flowmetricscsv:")
        print(exception)
        
        print("🪲 If the problem cannot be solved, consider opening an issue on GitHub: https://github.com/LetPeopleWork/FlowMetricsCSV/issues 🪲")

if __name__ == "__main__":    
    main()