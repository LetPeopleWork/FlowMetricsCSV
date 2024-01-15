from WorkItem import WorkItem

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import numpy as np
import pandas as pd

from collections import Counter

import os

class FlowMetricsService:    

    def __init__(self, show_plots, charts_folder):
        self.show_plots = show_plots
        self.charts_folder = charts_folder

        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)

       
    def plot_cycle_time_scatterplot(self, items, history, percentiles, percentile_colors, chart_name):
        print("Creating Cycle Time Scatterplot with following config: History: {0}, Chart Name: {1}, Percentiles: {2}, Percentile Colors: {3}".format(history, chart_name, percentiles, percentile_colors))

        cycle_times = [item.cycle_time for item in items if item.cycle_time is not None]

        if not cycle_times:
            print("No closed work items for plotting.")
            return

        if history is not None:
            # Filter items based on the history parameter
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and item.started_date and start_date <= item.closed_date <= end_date]
            cycle_times = [item.cycle_time for item in items if item.cycle_time is not None]
            dates = [item.closed_date.date() for item in items]

        if not cycle_times:
            print("No closed work items within the specified history for plotting.")
            return

        plt.figure(figsize=(15, 9))
        plt.scatter(dates, cycle_times)
        plt.title("Cycle Time Scatterplot")
        plt.xlabel("Work Item Closed Date")
        plt.ylabel("Cycle Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        # Calculate percentiles
        percentile_values = np.percentile(cycle_times, percentiles)

        # Plot percentile lines
        for value, label, color in zip(percentile_values, percentiles, percentile_colors):
            plt.axhline(y=value, color=color, linestyle='--', label=f'{label}th Percentile ({int(value)} Days)')

        plt.legend()

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()

    def plot_work_item_age_scatterplot(self, items, history, x_axis_lines, x_axis_line_colors, chart_name):
        print("Creating Work Item Scatterplot with following config: History: {0}, Chart Name: {1}, X-Axis Lines: {2}, X-Axis Line Colors: {3}".format(history, chart_name, x_axis_lines, x_axis_line_colors))
        work_item_ages = [item.work_item_age for item in items if item.work_item_age is not None]

        if not work_item_ages:
            print("No work items with age for plotting.")
            return

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(15, 9))

        dates = [item.started_date.date() for item in items if item.work_item_age is not None]

        # Plot Work Item Age as triangles
        plt.scatter(dates, work_item_ages, label='Work Item Age (days)', alpha=0.7)

        plt.title("Work Item Age Scatterplot with Cycle Time Percentiles")
        plt.xlabel("Work Item Started Date")
        plt.ylabel("Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        if history is not None:
            # Filter items based on the history parameter for calculating Cycle Time percentiles
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and start_date <= item.closed_date <= end_date]

        if len(items) < 1:
            print("No items within supplied history")
            return

        # Plot percentile lines for Cycle Time
        for value, color in zip(x_axis_lines, x_axis_line_colors):
            plt.axhline(y=value, color=color, linestyle='--', label=f'{value} Days')

        plt.legend()

        # Invert x-axis
        plt.gca().invert_xaxis()

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        
        if self.show_plots:
            plt.show()

    def plot_throughput_run_chart(self, items, history, chart_name, x_axis_unit='days'):
        print("Creating Throughput Run Chart with following config: History: {0}, Chart Name: {1}, Unit: {2}".format(history, chart_name, x_axis_unit))
        
        valid_units = ['days', 'weeks', 'months']
        if x_axis_unit not in valid_units:
            raise ValueError(f"The 'x_axis_unit' parameter should be one of {valid_units}.")
        
        # Filter items based on the history parameter
        start_date = datetime.today() - timedelta(days=history)
        closed_dates = [item.closed_date.date() for item in items if item.closed_date and start_date <= item.closed_date]

        if not closed_dates:
            print("No closed work items for plotting throughput.")
            return

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(15, 9))

        throughput_counts = Counter()

        for item in closed_dates:
            if x_axis_unit == 'days':
                key = item
            elif x_axis_unit == 'weeks':
                key = item.isocalendar()[1]
            elif x_axis_unit == 'months':
                key = item.month

            throughput_counts[key] += 1

        # Plot throughput as a bar chart
        if x_axis_unit == 'days':
            x_values = sorted(set(closed_dates))
        elif x_axis_unit == 'weeks':
            x_values = sorted(set(date.isocalendar()[1] for date in closed_dates))
        elif x_axis_unit == 'months':
            x_values = sorted(set(date.month for date in closed_dates))

        plt.bar(x_values, [throughput_counts[key] for key in x_values], color='blue', alpha=0.7, label='Throughput')

        plt.title("Throughput Run Chart")
        plt.xlabel(f"Work Item Closed Date ({x_axis_unit.capitalize()})")
        plt.ylabel("Number of Items Completed")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='upper left')

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()
            
    def plot_work_in_process_run_chart(self, items, history, chart_name):
        print("Creating Work In Process Run Chart with following config: History: {0}, Chart Name: {1}".format(history, chart_name))

        if not items:
            print("No work items for plotting work in process.")
            return

        if history is not None:
            # Filter items based on the history parameter
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.started_date is not None and start_date <= item.started_date <= end_date]

        # Set default size to be wider (10 inches width and 6 inches height in this example)
        plt.figure(figsize=(15, 9))

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
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='upper left')

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()

    def plot_work_started_vs_finished_chart(self, work_items, history, started_color, closed_color, chart_name):
        print("Creating Work Started vs. finished chart with following config: History: {0}, Chart Name: {1}, Started Color: {2}, Closed Color: {3}".format(history, chart_name, started_color, closed_color))

        start_date = datetime.today() - timedelta(days=history)
        filtered_items = [item for item in work_items if item.started_date and start_date <= item.started_date]

        # Calculate counts based on weeks
        started_counts = {}
        closed_counts = {}

        for item in filtered_items:
            started_date_key = item.started_date.date().strftime('%Y-%W') if item.started_date else None
            closed_date_key = item.closed_date.date().strftime('%Y-%W') if item.closed_date else None

            if started_date_key:
                started_counts[started_date_key] = started_counts.get(started_date_key, 0) + 1

            if closed_date_key:
                closed_counts[closed_date_key] = closed_counts.get(closed_date_key, 0) + 1

        # Collect all unique date keys
        all_date_keys = set(started_counts.keys()) | set(closed_counts.keys())

        # Convert keys back to integers for plotting
        sorted_date_keys_int = [datetime.strptime(key + '-1', "%Y-%W-%u").date() for key in all_date_keys]

        # Sort the dates chronologically
        sorted_date_keys_int.sort()

        # Get counts for both started and closed, filling in zeros for missing dates
        started_values = [started_counts.get(key, 0) for key in all_date_keys]
        closed_values = [closed_counts.get(key, 0) for key in all_date_keys]

        # Calculate the center positions for the bars
        center_positions = [x for x in range(len(sorted_date_keys_int))]

        # Plot the bar chart with adjusted x-axis positions
        plt.figure(figsize=(15, 9))
        bar_width = 0.35
        plt.bar(center_positions, started_values, width=bar_width, color=started_color, alpha=0.7, label='Started')
        plt.bar([pos + bar_width for pos in center_positions], closed_values, width=bar_width, color=closed_color, alpha=0.7, label='Closed')
        plt.title("Work Started and Closed")
        plt.xlabel("Week of the Year")
        plt.ylabel("Number of Work Items")

        # Set x-axis labels based on the week of the year
        plt.xticks([pos + bar_width / 2 for pos in center_positions], labels=[date.strftime("%Y-%W") for date in sorted_date_keys_int], rotation=45, ha='right')
        
        plt.legend()

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()