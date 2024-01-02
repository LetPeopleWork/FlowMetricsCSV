from WorkItem import WorkItem

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from collections import Counter

import os

class FlowMetricsService:    
       
    def plot_cycle_time_scatterplot(self, items, history, plot=True):
        cycle_times = [item.cycle_time for item in items if item.cycle_time is not None]

        if not cycle_times:
            print("No closed work items for plotting.")
            return

        if history is not None:
            # Filter items based on the history parameter
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and start_date <= item.closed_date <= end_date]
            cycle_times = [item.cycle_time for item in items if item.cycle_time is not None]
            dates = [item.closed_date.date() for item in items]

        if not cycle_times:
            print("No closed work items within the specified history for plotting.")
            return

        plt.figure(figsize=(10, 6))
        plt.scatter(dates, cycle_times)
        plt.title("Cycle Time Scatterplot")
        plt.xlabel("Work Item Closed Date")
        plt.ylabel("Cycle Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        
        # Calculate percentiles
        percentiles = [50, 70, 85, 95]
        colors = ['red', 'orange', 'lightgreen', 'darkgreen']
        percentile_values = np.percentile(cycle_times, percentiles)

        # Plot percentile lines
        for value, label, color in zip(percentile_values, percentiles, colors):
            plt.axhline(y=value, color=color, linestyle='--', label=f'{label}th Percentile')

        plt.legend()

        # Save the plot as an image in the "Charts" folder next to the script
        script_path = os.path.dirname(os.path.abspath(__file__))
        charts_folder = os.path.join(script_path, 'Charts')

        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        plt.savefig(os.path.join(charts_folder, 'CycleTime.png'))

        if plot:
            plt.show()

    def plot_work_item_age_scatterplot(self, items, history, plot=True):
        work_item_ages = [item.work_item_age for item in items if item.work_item_age is not None]

        if not work_item_ages:
            print("No work items with age for plotting.")
            return

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(10, 6))

        dates = [item.started_date.date() for item in items if item.work_item_age is not None]

        # Plot Work Item Age as triangles
        plt.scatter(dates, work_item_ages, marker='^', color='orange', label='Work Item Age (days)', alpha=0.7)

        plt.title("Work Item Age Scatterplot with Cycle Time Percentiles")
        plt.xlabel("Work Item Started Date")
        plt.ylabel("Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        if history is not None:
            # Filter items based on the history parameter for calculating Cycle Time percentiles
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and start_date <= item.closed_date <= end_date]

        # Calculate percentiles for Cycle Time
        cycle_times = [item.cycle_time for item in items if item.cycle_time is not None]
        cycle_time_percentiles = [50, 85]
        colors = ["orange", "red"]
        cycle_time_percentile_values = np.percentile(cycle_times, cycle_time_percentiles)

        # Plot percentile lines for Cycle Time
        for value, label, color in zip(cycle_time_percentile_values, cycle_time_percentiles, colors):
            plt.axhline(y=value, color=color, linestyle='--', label=f'{label}th Percentile (Cycle Time)')

        plt.legend()

        # Invert x-axis
        plt.gca().invert_xaxis()

        # Save the plot as an image in the "Charts" folder next to the script
        script_path = os.path.dirname(os.path.abspath(__file__))
        charts_folder = os.path.join(script_path, 'Charts')

        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        plt.savefig(os.path.join(charts_folder, 'WorkItemAgeWithCycleTimePercentiles.png'))
        
        if plot:
            plt.show()

    def plot_throughput_run_chart(self, items, history, plot=True):
        closed_dates = [item.closed_date.date() for item in items if item.closed_date is not None]

        if not closed_dates:
            print("No closed work items for plotting throughput.")
            return

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(10, 6))

        if history is not None:
            # Filter items based on the history parameter
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and start_date <= item.closed_date <= end_date]

        throughput_counts = Counter(closed_dates)

        # Plot throughput as a bar chart
        plt.bar(sorted(set(closed_dates)), [throughput_counts[date] for date in sorted(set(closed_dates))], color='blue', alpha=0.7, label='Throughput')

        plt.title("Throughput Run Chart")
        plt.xlabel("Work Item Closed Date")
        plt.ylabel("Number of Items Completed")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        plt.legend(loc='upper left')

        # Save the plot as an image in the "Charts" folder next to the script
        script_path = os.path.dirname(os.path.abspath(__file__))
        charts_folder = os.path.join(script_path, 'Charts')

        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        plt.savefig(os.path.join(charts_folder, 'ThroughputRunChart.png'))
        
        if plot:
            plt.show()

    def plot_work_in_process_run_chart(self, items, history, plot=True):
        if not items:
            print("No work items for plotting work in process.")
            return

        if history is not None:
            # Filter items based on the history parameter
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if start_date <= item.started_date <= end_date]

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(10, 6))

        # Create a range of dates representing the specified history
        history_dates = pd.date_range(end_date - timedelta(days=history-1), end_date)

        # Count the number of items in process for each day
        wip_counts = Counter()

        for item in items:
            wip_counts[item.started_date.date()] += 1
            if item.closed_date:
                wip_counts[item.closed_date.date()] -= 1

        # Calculate cumulative counts
        cumulative_wip = np.cumsum([wip_counts[date] for date in history_dates.date])

        # Plot work in process as a step chart
        plt.step(history_dates.date, cumulative_wip, where='post', color='orange', alpha=0.7, label='Work In Process')

        plt.title("Work In Process Run Chart")
        plt.xlabel("Date")
        plt.ylabel("Number of Items In Process")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        plt.legend(loc='upper left')

        # Save the plot as an image in the "Charts" folder next to the script
        script_path = os.path.dirname(os.path.abspath(__file__))
        charts_folder = os.path.join(script_path, 'Charts')

        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

        plt.savefig(os.path.join(charts_folder, 'WorkInProgressRunChart.png'))

        if plot:
            plt.show()