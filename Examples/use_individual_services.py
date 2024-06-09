from FlowMetricsCSV.CsvService import CsvService
from FlowMetricsCSV.FlowMetricsService import FlowMetricsService

csv_service = CsvService()
flow_metrics_service = FlowMetricsService(False, "Charts")


csv_service.write_example_file("ExampleFile.csv", ";", "Activated Date", "Closed Date", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p", "Story Points", "ID")

items = csv_service.parse_items("ExampleFile.csv", ";", "Activated Date", "Closed Date", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p", "Story Points", "ID")

flow_metrics_service.plot_cycle_time_scatterplot(items, 90, [50, 70, 95], ["red", "orange", "lightgreen"], "Cycle Time Scatter Plot")