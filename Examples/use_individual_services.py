from FlowMetricsCSV.CsvService import CsvService
from FlowMetricsCSV.FlowMetricsService import FlowMetricsService

csv_services = CsvService()
flow_metrics_service = FlowMetricsService(False, "Charts")

items = csv_services.parse_items("ExampleFile.csv", ";", "Activated Date", "Closed Date", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p", "Story Points", "ID")

flow_metrics_service.plot_cycle_time_scatterplot(items, 90, [50, 70, 95], ["red", "orange", "lightgreen"], "Cycle Time Scatter Plot")