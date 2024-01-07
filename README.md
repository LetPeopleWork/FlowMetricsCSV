# Flow Metrics CSV
This is a script that visualizes the four measures of flow based on any csv file. It can be run offline, and all it needs is a csv file with the start and closing dates of the items. Items that are still in progress, have no value for the closed date. My hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of Flow Metrics.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of Flow Metrics comes when inspected on a regular base. The point of collecting data is to take action, so use this to make informed decisions about what you want to adjust! You can use this for free, hope it helps.

If you like it and use the script, I'm happy if I can mention you/your company in the readme or for an attribution on [LinkedIn](https://www.linkedin.com/in/huserben/).

## Download Files
In order to run the scripts, you need to download all the files in this repository. There are dependencies between the files so you cannot just download a single file. Please always use the full folder structure.

## Install Prerequisites
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

It should do two things:
1. Pop up 4 visualizations after each other (you have to close them for the script to continue)
2. Store the images in the folder "Charts" where you run the script from

## Configuration Options
In `FlowMetrics.py` the following default values are defined:

```
parser.add_argument("--FileName", default="ExampleFile.csv")
parser.add_argument("--Delimeter", default=";")
parser.add_argument("--StartedDateColumn", default="Activated Date")
parser.add_argument("--ClosedDateColumn", default="Closed Date")
parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
parser.add_argument("--History", default="90")
parser.add_argument("--ShowPlots", default=False, action=argparse.BooleanOptionalAction)
```

You can overwrite them either by changing the python file or by supplying specific options via the command line: `python .\FlowMetrics.py --History 30`
I would recommend changing the values that don't change often (for example the file name) in code, while for others like History to supply them via the command line, so you can easily rerun it with different configurations.

### Arguments
Name | Description |
--- | --- |
--FileName | The name of the csv file to be used for the simulation. Default is "ExampleFile.csv". Can be a relative path (using '.') or an absolute one |
--Delimeter | The delimeter which is used in the specified csv file. Default is ; |
--StartedDateColumn | The name of the column in the csv file that contains the started date. Default is "Activated Date". |
--ClosedDateColumn | The name of the column in the csv file that contains the closed date. Default is "Closed Date". |
--DateFormat | The format of the dates in the csv file. Default is "%m/%d/%Y %I:%M:%S %p". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--History | The number of days of history to be used for the simulation. Default is "90". |
--ShowPlots | Supply this parameter to get an interactive view of the charts while they are being created |

# Charts
Following you find a list of charts that will be created by the tool and how you can use them.

## Cycle Time Scatterplot
This chart plots the Cycle Time for each item in the selected history. On the X-Axis you can see the _Closed Date_ of each item, while the Y-Axis is the Cycle Time of the specific item.

The Cycle Time is calculated as follows:
> Cycle Time = (Closed Date - Start Date) + 1

The "+1" comes from the fact that we assume a cycle time of 1 day when an item is started and closed on the same day. That means the minimum Cycle Time is 1.
Items that are not yet closed (no Closing Date) don't have a Cycle Time and will not be shown in this Chart.

The chart also includes four different percentile lines: 50, 70, 85, and 95. They indicate how many items were closed in x days or less.

### Example
![CycleTime](https://github.com/LetPeopleWork/FlowMetricsCSV/assets/5486874/7f1ac8f0-a6bf-4eae-9506-a8a218ff2328)

In this chart, you can see there is one outlier (20+ days). 85% of all the items were closed in 8 days or less, and 70% of all items were closed in 6 days or less.

You can use the chart to spot patterns (for example, are we closing many items on a single day, which would indicate some kind of bigger batches) or outliers (are there items that took way longer than the rest).
Also, you can use the percentiles to give you guidance for [Right-Sizing](https://www.youtube.com/watch?v=kB3FYda7SSM) your work items. In the example above, you might decide with your team that the 85th percentile might be a good target for your team. You can set your "Service Level Expectation" (SLE) to this number, so you can communicate this also with stakeholders: 85% of all the items will be done within 8 days or less (once they are started). Instead of estimating time or effort (for example using Story Points), you can simply size the items by asking: Will we manage this in 8 days or less? If the answer is, you're good. If not, you might have discussions on how to achieve this or how it could be broken into smaller pieces.

## Work Item Age Scatterplot
This chart plots the Work Item Age for each item in the selected history. On the X-Axis, you can see the _Start Date_ of each item, while the Y-Axis is the Work Item Age of the specific item. The scatterplot also includes the percentile lines from the *Cycle Time*. This is useful to spot when items are approaching our SLEs or are even already beyond them.

If items are started, but not yet finished, they won't have a Cycle Time. Instead, they have a "Work Item Age". The calculation of Work Item Age is done similar to the Cycle Time, but instead of the Closing Date, we take today's date:
> Work Item Age = (Today - Start Date) + 1

Again we use the "+1" because the minimum age is 1 day. So as soon as we start to work on an item, its age becomes 1.

### Example

![WorkItemAgeWithCycleTimePercentiles](https://github.com/LetPeopleWork/FlowMetricsCSV/assets/5486874/e4827083-1982-494f-a2f2-0905d0b319d2)

In this chart, you can see that quite a lot of items are beyond our percentile lines. There is one item that is in progress already 80 days, while two more are between 20 and 40 days in progress. A team should find ways to close those items first, before focusing on the items that are near the percentile lines.

A way to use this chart can also be to check it out during daily meetings (if you have them) and discuss the oldest items and how progress can be made on them. If you were to use the 85th percentile as SLE, you should start discussing how to close the item once it hits the 50th percentile line.

## Throughput Run Chart
The chart shows the Throughput over the history specified. On the X-Axis you can see each day, while on the Y-Axis you can see how many items were closed on this day.

The run chart can help spot whether the team is using bigger batches to close items (for example everything gets closed at the end of a Sprint instead of continuously). The goal should be to have a steady Throughput with no big outliers in either direction. The more "even" this is, the more predictable your team is. This also serves as input for the Monte Carlo Simulation, if you run them. The more steady this is, the more precise your forecasts will work.

### Example
![ThroughputRunChart](https://github.com/LetPeopleWork/FlowMetricsCSV/assets/5486874/f97ac643-ced3-43d1-a61b-853fe3916a51)

In the above example, you can spot that there are not many periods of days where nothing was completed. As weekends are included, some "gaps" are expected. Also towards the right side, you can see a bigger gap, but most likely this is due to the holiday break at the end of December.

And while there are some "outliers" where 4 or 5 items were closed on the same day, it seems that the work is flowing through rather steadily in this team.

## Work In Process Run Chart
This chart shows the total amount of Work In Progress over the specified history. On the X-Axis you can see each day, while on the Y-Axis you can see the WIP total for that day. On [Kanban Practice](https://kanbanguides.org/english/) is to "Controlling Work In Progress" and this chart helps you to spot outliers. Are we steadily increasing or decreasing WIP? It allows us to take action if we spot this, for example by saying that we don't start anything new until we're under a certain Threshold.

An item counts to the WIP if it's started but not closed, meaning it has a Started but no Closing Date.

### Example

![WorkInProgressRunChart](https://github.com/LetPeopleWork/FlowMetricsCSV/assets/5486874/dbc6848d-21f7-41b8-b578-43db3c83ef2f)

In the above example, you can see that around the start of December, the WIP increased a lot, before slowly decreasing again. 
