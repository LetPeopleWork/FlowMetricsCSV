import sys
from FlowMetricsCSV.main import main

config_file_path = 'ExampleConfig.json'

sys.argv = ['flowmetricscsv', '--ConfigFileNames', config_file_path]

main()