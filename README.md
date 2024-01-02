# Flow Metrics CSV
This is a script that visualizes the four measures of flow based on any csv file. It can be run offline, and all it needs is a csv file with the start and closing dates of the items. Items that are still in progress, have no value for the closed date. My hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of Flow Metrics.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of Flow Metrics comes when inspected on a regular base. The point of collecting data is to take action, so use this to make informed decisions about what you want to adjust! You can use this for free, hope it helps.

If you like it and use the script, I'm happy if I can mention you/your company in the readme or for an attribution on [LinkedIn](https://www.linkedin.com/in/huserben/).

## Download Files
In order to run the scripts, you need to download all the files in this repository. There are dependencies between the files so you cannot just download a single file. Please always use the full folder structure.

## Install Prerequisites
Make sure you have python 3.x installed on your system and it's available via your PATH variable.

Then run `python -m pip install -r .\requirements.txt` from this directory to install the packages.

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
parser.add_argument("--FileName", default=".\\ExampleFile.csv")
parser.add_argument("--Delimeter", default=";")
parser.add_argument("--StartedDateColumn", default="Activated Date")
parser.add_argument("--ClosedDateColumn", default="Closed Date")
parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
parser.add_argument("--History", default="90")
```

You can overwrite them either by changing the python file or by supplying specific options via command line: `python .\FlowMetrics.py --History 30`
I would recommend to change the values that don't change often (for example the file name) in code, while for others like History to supply them via command line, so you can easily rerun it with different configurations.

### Arguments
Name | Description |
--- | --- |
--FileName | The name of the csv file to be used for the simulation. Default is ".\\ExampleFile.csv". Can be a relative path (using '.') or an absolute one |
--Delimeter | The delimeter which is used in the specified csv file. Default is ; |
--StartedDateColumn | The name of the column in the csv file that contains the started date. Default is "Activated Date". |
--ClosedDateColumn | The name of the column in the csv file that contains the closed date. Default is "Closed Date". |
--DateFormat | The format of the dates in the csv file. Default is "%m/%d/%Y %I:%M:%S %p". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--History | The number of days of history to be used for the simulation. Default is "90". |

# Charts
TO DO

## Cycle Time Scatterplot

## Work Item Age Scatterplot

## Throughput Run Chart

## Work In Process Run Chart