import sys
from FlowMetricsCSV.CsvService import CsvService
from FlowMetricsCSV.main import main

csv_service = CsvService()

# Generate sample csv
csv_service.write_example_file("ExampleFile.csv", ";", "Activated Date", "Closed Date", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p", "Story Points", "ID")

config_file_path = 'ExampleConfig.json'
sys.argv = ['flowmetricscsv', '--ConfigFileNames', config_file_path]

main()