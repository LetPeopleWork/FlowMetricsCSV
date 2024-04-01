# Flow Metrics CSV
This is a script that visualizes the four measures of flow based on any csv file. It can be run offline, and all it needs is a csv file with the start and closing dates of the items. Items that are still in progress, have no value for the closed date. My hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of Flow Metrics.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of Flow Metrics comes when inspected on a regular base. The point of collecting data is to take action, so use this to make informed decisions about what you want to adjust! You can use this for free, hope it helps.

If you like it and use the script, I'm happy if I can mention you/your company in the readme or for an attribution on [LinkedIn](https://www.linkedin.com/in/huserben/).

## Download Files
In order to run the scripts, you need to download all the files in this repository. There are dependencies between the files so you cannot just download a single file. Please always use the full folder structure.

## Install Prerequisites
Make sure you have python 3.x installed on your system and it's available via your PATH variable. You can check this by running `python --version` on your terminal. If it works without error, you have python installed and ready. If not, you can download it from the [official Python Website](https://www.python.org/downloads/).

**Important:** It can be that you have to use `python3 --version`. If this is the case, please use always `python3` instead of `python` in the following commands.

Once you have made sure python is installed, you can fetch the required python packages:
Run `python -m pip install -r .\requirements.txt` from the directory that contains the scripts.

**Important:** If you are on Linux or MacOS, the paths work differently. Use "/" instead of "\" for all the commands that follow. So the above command would look like this for MacOS/Linux:
`python -m pip install -r ./requirements.txt`

## Create Flow Metrics Visulization
To create the visulizations with this script, you need various inputs. First and foremost, you need to provide a csv file that includes the date when an item was started and closed (unless it's still in progress). The csv can contain other information, but it's not needed nor relevant for any of the visulizations. Using the "history" parameter, you can define which perioud you want to visualize. Do you want to see the last 30 days or rather the last 90 days?

### Run using the example values
The repo comes with an example configuration including an example csv file.
Simply run `python .\FlowMetrics.py` to run the visualization. 

If it runs successfully, it will store all the generated charts in a folder called "Charts" next to your script location.

## Configuration
In the [config.json](https://github.com/LetPeopleWork/FlowMetricsCSV/blob/main/config.json) file you can see the default configuration. There are general settings and configurations per chart. Below you can find a summary of the various options.

<details>
  <summary>Sample Configuration</summary>
  ```json
{
    "general": {
        "fileName": "ExampleFile.csv",
        "delimeter": ";",
        "startedDateColumn": "Activated Date",
        "closedDateColumn": "Closed Date",
        "startDateFormat": "%m/%d/%Y %I:%M:%S %p",
        "closedDateFormat": "",
        "estimationColumn": "Story Points",
        "itemTitleColumn": "ID",
        "chartsFolder": "Charts",
        "showPlots": false
    },
    "cycleTimeScatterPlot": {
        "generate": true,
        "history": 30,
        "chartName": "CycleTime.png",
        "percentiles": [50, 70, 85, 95],
        "percentileColors": ["red", "orange", "lightgreen", "darkgreen"]
    },
    "workItemAgeScatterPlot": {
        "generate": true,
        "history": 30,
        "chartName": "WorkItemAge.png",
        "xAxisLines": [5, 10],
        "xAxisLineColors": ["orange", "red"]
    },
    "throughputRunChart": {
        "generate": true,
        "history": 90,
        "unit": "days",
        "chartName": "Throughput.png"
    },
    "workInProcessRunChart": {
        "generate": true,
        "history": 30,
        "chartName": "WorkInProcess.png"
    },
    "startedVsFinishedChart": {
        "generate": true,
        "history": 90,
        "chartName": "StartedVsFinished.png",
        "startedColor": "orange",
        "closedColor": "green"
    },
    "estimationVsCycleTime": {
        "generate": false,
        "history": 90,
        "chartName": "EstimationVsCycleTime.png",
        "estimationUnit": "Story Points"
    }
}
  ```
</details>

### General

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| FileName               | The name of the CSV file you want to use as input. Can be a relative path from the script location (like in the example) or a full path if the files are somewhere else.             | ExampleFile.csv   |
| Delimeter              | The delimiter used in the CSV file   | ;                  |
| StartedDateColumn      | The name of the column in the csv file that contains the started date       | Activated Date     |
| ClosedDateColumn       | The name of the column in the csv file that contains the closed date          | Closed Date        |
| StartDateFormat        | The format of the start dates in the csv file. Default is "%m/%d/%Y %I:%M:%S %p". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT)       | %m/%d/%Y %I:%M:%S %p|
| ClosedDateFormat       | The format of the closed dates in the csv file. If not set (default), the same format as specified for the start date is used. Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT)          | None |
| estimationColumn       | The name of the column in the csv file that contains the estimations (optional). This is needed if you want to plot a chart where you compare estimates vs. cycle-time.          | Story Points        |
| itemTitleColumn       | The name of the column in the csv file that contains the title of the items (optional). This can be anything to identify the item, like an ID or some other text. If set, it will display the text next to the bubbles in the charts. Note that the shorter the text, the easier it is to read. Long texts will overlap.          | ID        |
| ChartsFolder           | Folder path for the folder where the charts should be saved. Can be relative to the script location (like the default) or a full path to a folder. Folder does not need to exist, it will be created as part of the script.               | Charts             |
| ShowPlots              | If set to true, the script will stop and show you an interactive version of the chart before continuing.                | false              |

### Cycle Time Scatter Plot

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified.        | true               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 30                 |
| ChartName              | File name of the chart.     | CycleTime.png      |
| Percentiles            | List of which percentiles should be shown in the chart. Can be any value from 1 to 100.     | [50, 70, 85, 95]    |
| PercentileColors       | Colors for the percentiles defined. The amount has to match with what you specified above. Colors are associated by sequence. | [red, orange, lightgreen, darkgreen]|

### Work Item Age Scatter Plot

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified.         | true               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 30                 |
| ChartName              | File name of the chart.       | WorkItemAge.png    |
| XAxisLines             | List of which lines should be shown on the x-axis (in days). This can be useful to track if your items approach their [Service Level Expectation](https://kanbanguides.org/english/).      | [5, 10]            |
| XAxisLineColors        | Colors for corresponding X-axis lines. The amount has to match with what you specified above. Colors are associated by sequence. | [orange, red]      |

### Throughput Run Chart

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified.         | true               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 90                 |
| Unit                   | Which grouping is applied. Possible options are 'days', 'weeks', and 'months'    | days               |
| ChartName              | File name of the chart.               | Throughput.png     |

### Work In Process Run Chart

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified.         | true               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 30                 |
| ChartName              | File name of the chart.                 | WorkInProcess.png  |

### Started Vs FinishedChart

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified.         | true               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 90                 |
| ChartName              | File name of the chart.          | StartedVsFinished.png|
| StartedColor           | Color for started items on the chart  | orange             |
| ClosedColor            | Color for closed items on the chart   | green              |


### Estimation Vs CycleTime

| Name                   | Description                          | Default Value      |
|------------------------|--------------------------------------|--------------------|
| Generate               | Whether to generate the chart at all. If set to false, no further settings need to be specified. If enabled, `estimationColumn` must be set and available in the CSV.         | false               |
| History                | Defines how much data should be used. It's always calculated from today backwards. The value is in days.      | 90                 |
| ChartName              | File name of the chart.          | EstimationVsCycleTime.png|
| estimationUnit         | Unit of estimation that will be visible on the chart. Examples: Story Points, Hours, Ideal Days etc.          | Story Points |

## Running the Script with different/multiple Configurations
If not specified otherwise, the _config.json_ will be used. However, you can also override which config file should be used by specifying it as part of the command line when running the script:
`python .\FlowMetrics.py --ConfigFileNames ".\myOtherConfig.json"`

That way, you can have multiple configurations that you can use to create different charts. For example for different teams or different item types (for example if you want to visualize Epics differently than other work items).
Each configuration is independent and can work against different input files. If you want to generate many charts at once with different configurations, you can also specify multiple configuration files:
`python .\FlowMetrics.py --ConfigFileNames ".\TeamA_Config.json" ".\TeamB_Config.json" ".\TeamC_Config.json"`

This will generate you three sets of charts as per the individual configurations specified.
**Note:** Make sure to specify different folders or chart names in the respective configs, as otherwise they will be overwritten.

# How to use the created charts?
You find more information on this in the [wiki](https://github.com/LetPeopleWork/FlowMetricsCSV/wiki)