from WorkItem import WorkItem

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import adjustText as adjustText

import numpy as np
import pandas as pd

from collections import Counter

import os

class FlowMetricsService:    

    def __init__(self, show_plots, charts_folder):
        self.show_plots = show_plots
        self.charts_folder = charts_folder

        self.current_date = datetime.now().strftime('%d.%m.%Y')

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
        
        texts = []
        for item in items:
            text = plt.text(item.closed_date.date(), item.cycle_time, item.item_title, ha='center')
            texts.append(text)

        # Adjust text to avoid overlap
        adjustText.adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))
        
        plt.title("Cycle Time Scatterplot")
        plt.xlabel("Work Item Closed Date")
        plt.ylabel("Cycle Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

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
        
        texts = []
        for item in items:
            work_item_age = item.work_item_age
            
            if work_item_age:
                text = plt.text(item.started_date.date(), work_item_age, item.item_title, ha='center')
                texts.append(text)

        # Adjust text to avoid overlap
        adjustText.adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))

        plt.title("Work Item Age Scatterplot with Cycle Time Percentiles")
        plt.xlabel("Work Item Started Date")
        plt.ylabel("Time (days)")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

        if history is not None:
            # Filter items based on the history parameter for calculating Cycle Time percentiles
            end_date = datetime.today()
            start_date = end_date - timedelta(days=history)
            items = [item for item in items if item.closed_date and start_date <= item.closed_date <= end_date]

        if len(items) > 0:            
            for value, color in zip(x_axis_lines, x_axis_line_colors):
                plt.axhline(y=value, color=color, linestyle='--', label=f'{value} Days')
        else:
            print("No closed items, skipping cycle time percentiles in WIA Scatterplot")

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

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

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

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

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
                
                # Make sure we have the same keys in both dictionaries - keep the existing value
                closed_counts[started_date_key] = closed_counts.get(started_date_key, 0) + 0

            if closed_date_key:
                closed_counts[closed_date_key] = closed_counts.get(closed_date_key, 0) + 1

                # Make sure we have the same keys in both dictionaries - keep the existing value
                started_counts[closed_date_key] = started_counts.get(closed_date_key, 0) + 0

        # Sort dictionaries
        key_function = lambda x: x[0]

        sorted_started_counts = dict(sorted(started_counts.items(), key=key_function))
        sorted_closed_counts = dict(sorted(closed_counts.items(), key=key_function))

        # Calculate the center positions for the bars
        center_positions = [x for x in range(len(started_counts))]

        # Plot the bar chart with adjusted x-axis positions
        plt.figure(figsize=(15, 9))
        bar_width = 0.35
        plt.bar(center_positions, sorted_started_counts.values(), width=bar_width, color=started_color, alpha=0.7, label='Started')
        plt.bar([pos + bar_width for pos in center_positions], sorted_closed_counts.values(), width=bar_width, color=closed_color, alpha=0.7, label='Closed')

        plt.title("Work Started and Closed")
        plt.xlabel("Week of the Year")
        plt.ylabel("Number of Work Items")

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

        # Set x-axis labels based on the week of the year
        plt.xticks([pos + bar_width / 2 for pos in center_positions], labels=sorted_started_counts.keys(), rotation=45, ha='right')
        
        plt.legend()

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()

    def plot_estimation_vs_cycle_time_scatterplot(self, items, history, chart_name, estimation_unit):
        print("Creating Estimation vs. Cycle Time Scatterplot with the following config: History: {0}, Chart Name: {1}, Estimation Unit: {2}".format(history, chart_name, estimation_unit))

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
            estimations = [item.estimation for item in items if item.cycle_time and item.estimation is not None]

        if not cycle_times:
            print("No closed work items within the specified history for plotting.")
            return


        plt.figure(figsize=(15, 9))
        plt.scatter(estimations, cycle_times)
        
        texts = []
        for item in items:
            text = plt.text(item.estimation, item.cycle_time, item.item_title, ha='center')
            texts.append(text)

        # Adjust text to avoid overlap
        adjustText.adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))
        
        plt.title("Estimation vs. Cycle Time")
        plt.xlabel("Estimation ({0})".format(estimation_unit))
        plt.ylabel("Cycle Time (days)")
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()
            
    def plot_throughput_process_behaviour_chart(self, work_items, baseline_start_date, baseline_end_date, history, chart_name):        
        baselin_closed_items = self.get_throughput_history_for_date_range(baseline_start_date, baseline_end_date, work_items)
        
        baseline_values = list(baselin_closed_items.values())
        (baseline_average, unpl, lnpl) = self.caclulate_average_and_limits(baseline_values)
        
        start_date = datetime.today() - timedelta(days=history)
        throughput_data = self.get_throughput_history_for_date_range(start_date, datetime.today(), work_items)
        
        dates = list(throughput_data.keys())
        throughput_values = list(throughput_data.values())

        # Plot throughput data
        plt.figure(figsize=(15, 9))
        plt.plot(dates, throughput_values, marker='o', linestyle='-', color='b')

        # Plot baseline average, unpl, and lnpl as horizontal lines
        plt.axhline(y=baseline_average, color='r', linestyle='--', label='Average')
        plt.axhline(y=unpl, color='g', linestyle='--', label='Upper Natural Process Limit (UNPL)')
        
        if (lnpl > 0):
            plt.axhline(y=lnpl, color='y', linestyle='--', label='Lower Natural Process Limit (LNPL)')

        # Set x-axis label and rotate x-axis ticks for better readability
        plt.xlabel('Date')
        plt.xticks(rotation=45)

        # Set y-axis label
        plt.ylabel('Throughput')

        # Set chart title and legend
        plt.title("Throughput X Chart")
        plt.legend()
        
        # Print Current Date
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')

        chart_file_path = os.path.join(self.charts_folder, chart_name)
        print("Storing file at {0}".format(chart_file_path))
        plt.savefig(chart_file_path)

        if self.show_plots:
            plt.show()
        
    def get_throughput_history_for_date_range(self, start_date, end_date, work_items):
        closed_items_count = {}
        
        date_range = (end_date - start_date).days + 1
        
        for index in range(date_range):
            closed_items_count[index] = 0
        
        for item in work_items:
            if item.closed_date and start_date <= item.closed_date <= end_date:
                index = (item.closed_date - start_date).days
                
                closed_items_count[index] += 1
                
        return closed_items_count
    
    def caclulate_average_and_limits(self, baseline_values):
        baseline_average = self.calculate_mean(baseline_values)
        moving_ranges = self.calculate_moving_ranges(baseline_values)
        moving_range_mean = self.calculate_mean(moving_ranges)
        (unpl, lnpl) = self.calculate_natural_process_limits(baseline_average, moving_range_mean)
        
        print("Baseline Average: {0}".format(baseline_average))
        print("Upper Natural Process Limit: {0}".format(unpl))
        print("Lower Natural Process Limit: {0}".format(lnpl))
        
        return (baseline_average, unpl, lnpl)
        
    def calculate_mean(self, values):
        mean = sum(values) / len(values)
        
        return mean
        
    def calculate_moving_ranges(self, values):
        moving_ranges = []
        for i in range(1, len(values)):
            moving_range = abs(values[i] - values[i-1])
            moving_ranges.append(moving_range)
        return moving_ranges
    
    def calculate_natural_process_limits(self, baseline_average, baseline_moving_range_average):
        unpl = baseline_average + (2.66 * baseline_moving_range_average)
        lnpl = baseline_average - (2.66 * baseline_moving_range_average)
        
        if lnpl < 0:
            lnpl = 0
        
        return (unpl, lnpl)