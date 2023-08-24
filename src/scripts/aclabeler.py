# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: ac-monitor
#     language: python
#     name: ac-monitor
# ---

# %% [markdown]
# # Experiements

# %%
# import pandas as pd

# create a sample DataFrame with a DatetimeIndex
# date_rng = pd.date_range(start='2020-01-01', end='2020-01-31', freq='D')
# df = pd.DataFrame(date_rng, columns=['date'])
# df.set_index('date', inplace=True)
# df

# %%
# make sure start is not before the beginning of the index
# start = pd.to_datetime('2019-12-01')
# if start < df.index.min():
#     start = df.index.min()

# %%
# now we can safely use df.loc[start:end]
# end = pd.to_datetime('2020-02-15')
# result = df.loc[start:end]

# %%
# start

# %%
# result

# %% [markdown]
# # Label segments of time series for abnormality detection training

# %% [markdown]
# This program provides interactive means to select segments of time series and label them, and save the labeled segments into files.

# %% [markdown]
# ## import

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
from IPython.display import clear_output

# %%
from importlib import reload

# import os
import sys
sys.path.insert(0, '../scripts') # for aclabeler.py moved to src/scripts

# %%
import ac_utils as acu

# %%
reload(acu)


# %% [markdown]
# ## Class ACLabeler
#
# Using this class as a namespace for the implementation of the interactive labeling.

# %% [markdown]
# ### Notes on ACLabeler.\_\_init__
#
# Initialize the object of ACLabeler, based on the input of the raw temperature data for a location, loading self.raw_temperatures_df, and computing the min or max of the temperatures.

# %% [markdown]
# ### Notes on ACLabeler.label
#
# Given the input of a starting time, and the required number of temperature data points from the start, start the interactive labeling,
# saving the labeled data according to the value of self.labeled_base_name, with suffix to avoid overriding pre-existing labeled data.

# %% [markdown]
# ### ACLabeler (proper)
#
#

# %%
class ACLabeler:
    """
    Training example labeler for temperature time series data.
    """

    def __init__(self, root_data_dir: str, raw_temperatures_name: str, labeled_base_name: str,
                 timestamp_col: str = '_time', temperature_col: str = 'Temperature', label_col: str = 'abnormality',
                 normal_label: object = 0, abnormal_label: object = 1,
                 save_fig_path: str = '', number_of_data_points_required: int = 16,
                 ideal_temperature: float = 75, critical_temperature: float = 90):
        """
        Initialize parameters for labeler.

        : param root_data_dir: the root directory containing data
        : param labeled_base_name: the base name of the file containing labeledtime intervals data
                                       with the label column and the extracted temperature time-series data points.
                                       The intervals are defined for each location.
        : param raw_temperatures_name: the base name of the file containing raw temperature data, from which data falling to the time intervals will be labeled
        : param timestamp_col: Column containing timestamps in the raw_temperatures dataframe
        : param temperature_col: Column containing temperatures in the raw_temperatures dataframe
        : param label_col: Column containing labels for each time interval in the labeled_time_intervals dataframe
        : param normal_label: Label for normal time_intervals. Defaults to 0
        : param abnormal_label: Label for abnormal time_intervals. Defaults to 1
        """
        # Validate the required number of data points
        if number_of_data_points_required < 1:
            raise ValueError('number_of_data_points_required must be positive')

        self.root_data_dir          = root_data_dir
        self.labeled_base_name           = labeled_base_name
        self.raw_temperatures_name  = raw_temperatures_name
        
        # self.labeled_zip = root_data_dir + labeled_base_name + '.csv' + '.zip'
        self.labeled_dir = root_data_dir + "labeled/"
        self.abonormal_labeled_file_base_name = f'{labeled_base_name}-abnormal' # the base qualified name
        self.normal_labeled_file_base_name = f'{labeled_base_name}-normal'      # the base qualified name
        self.location_col    = 'Location'
        self.start_col       = 'Start'
        self.end_col         = 'End'

        self.timestamp_col   = timestamp_col
        self.temperature_col = temperature_col
        self.label_col       = label_col
        self.normal_label    = normal_label
        self.abnormal_label  = abnormal_label
        self.save_fig_path_full = self.root_data_dir+save_fig_path
        self.number_of_data_points_required = number_of_data_points_required
        self.ideal_temperature = ideal_temperature
        self.critical_temperature = critical_temperature

        # Preload temperature data. This may be time consuming. But it's necessary to get the min and max temperatures for all locations.
        try:
            print(f'Loading {raw_temperatures_name} all raw temperature data...')
            self.raw_temperatures_df = pd.read_csv(
                root_data_dir + raw_temperatures_name,
                index_col=timestamp_col,
                converters={timestamp_col: pd.to_datetime}
            )
            
            # Important temperature values
            self.min_temp = min(self.raw_temperatures_df[self.temperature_col])
            self.max_temp = max(self.raw_temperatures_df[self.temperature_col])
        except FileNotFoundError:
            print(f'Unable to load temperature data for {root_data_dir + raw_temperatures_name + ".zip"}, created empty temperature DataFrame')
            return

    def reset(self):
        # Reset the labeled data
        # Besides the columns of location, start, end, and label,
        # prepend the columns of the time series data points
        self.labeled_abnormal = self.embpty_labeled_df()
        self.labeled_normal   = self.embpty_labeled_df()

        self.previous_label = None

    def get_remaining_temperatures(self, start_time):
        # Find the starting row in the raw_temperatures_df for labeling
        if start_time == '':
            start_index = 0
        else:
            start_index = self.raw_temperatures_df.index.get_loc(pd.to_datetime(start_time), method='nearest')
        return self.raw_temperatures_df.iloc[start_index:]

    def flip_labeled(self):
        def transfer(from_df, to_df):
            last_row = from_df.iloc[-1] # copy the last row from from_df
            last_row[self.label_col] = new_label # change the label

            # transfer the last row to to_df
            # to_df = to_df.append(last_row)
            to_df = pd.concat([to_df, last_row.to_frame().T], axis=0)
            # remove the last row from from_df
            from_df = from_df.iloc[:-1]
            return from_df, to_df

        if self.previous_label == self.abnormal_label:
            new_label = self.normal_label
            self.labeled_abnormal, self.labeled_normal = transfer(self.labeled_abnormal, self.labeled_normal)
        else:
            new_label = self.abnormal_label
            self.labeled_normal, self.labeled_abnormal = transfer(self.labeled_normal, self.labeled_abnormal)
        # update self.previous_label
        self.previous_label = new_label



    def label(self,
              autosave_freq: int = 10, 
              context_before_hrs: float = 2.0, context_after_hrs: float = 2.0, 
              show_abnormality_score: bool = True,
              start_time: str = '',
              ):
        """
        Main labeling routine. Visualize the temperature segment starting from start_time for number_of_data_points_required in self.raw_temperatures_df
        and prompt the user to label the data. 
        Continue the labeling with the next timestamp in the self.raw_temperatures_df until the end of the data or the human labeler's termination.

        :param context_before_hrs: Number of hours before the current time interval to visualize. Defaults to 2.0
        :param context_after_hrs: Number of hours after the current time interval to visualize. Defaults to 2.0
        :param ideal_temp: Ideal temperature, for visualization purposes. Defaults to 75.0
        :param critical_temp: Critical temperature - temperatures above this value indicate a potential AC failure 
                              - for visualization and abnormality score calculation purposes. Defaults to 90.0
        :param show_abnormality_score: Show "abnormality score" (see comments in function). Defaults to True
        : param start_time: Start labeling at this time in format of data and time stamp recqgnizable by DateTime. 
                            Defaults to empty string, which means start at the beginning.
        :param number_of_data_points_required: require this many temperature data points in each time interval. Must be positive. Defaults to 0
        :param autosave_freq: Automatically save after this many labelings. Defaults to 10
        :param save_fig_path: Path to save temperature visualizations to. Defaults to current directory

        :return: Labeled time_intervals DataFrame
        """
        sns.set_theme()  # Set pyplot theme

        remaining_temperatures = self.get_remaining_temperatures(start_time)

        self.reset() # Reset the labeled dataframes, and the previous label
        user_input = 'x' # for next record

        # initalize for the potentially unbounded
        interval_temperatures, interval_start, interval_end, interval_loc, fig = None, None, None, None, None

        try:
            while not remaining_temperatures.empty:
                clear_output(wait=True)  # Clear previous output
                # Autosave
                self.save_when_enough(autosave_freq)

                if user_input in ['n', 'a', 'x']: # ready for the next labeling
                    # Do not label remaining_time_intervals that do not contain enough data points
                    # Maybe, a more relaxed approach is to get enough from the interval if possible.
                    interval_temperatures = remaining_temperatures.iloc[:self.number_of_data_points_required]
                    if (len(interval_temperatures) < self.number_of_data_points_required): # not enough data points
                        print(f'Not enough data points in the interval: {len(interval_temperatures)}')
                        break # break the while loop

                    # Get the interval location start time, and end time
                    # extract interval_loc from self.raw_temperatures_name
                    interval_loc = interval_temperatures[self.location_col].iloc[0] # self.raw_temperatures_name.split('_')[1].split('.')[0]
                    interval_start = interval_temperatures.index[0]
                    interval_end = interval_temperatures.index[-1]

                    # Plot temperature curve
                    fig, ax = self.plot_interval(interval_loc, interval_start, interval_temperatures, interval_end,
                                                 context_before_hrs=context_before_hrs, context_after_hrs=context_after_hrs,
                                                 save_fig=None)

                    # Calculate "abnormality score": the sum of the square of the difference between the max temp and
                    # every temperature above the max temp. Idea taken from Floyd Fang
                    if show_abnormality_score:
                        ab_score = sum(max((temp - self.critical_temperature), 0)**2 for temp in interval_temperatures.iloc[self.temperature_col])
                        # questionable logic: why the last row is dropped? by YS?
                        # I removed the drop last row logic, let's see if it works. by YS
                        print('Abnormality score: {:.2f}\n'.format(ab_score))

                commands_for_labeling = "n = normal, a = abnormal," if user_input in ['n', 'a', 'x'] else "" # ready for labeling
                undo_command = 'u = Flip previous label, ' if self.previous_label is not None else '' # possible to do undo
                user_input = input(
                    f"Enter label ({commands_for_labeling} {undo_command} p = Check progress, s = Save labels, i = Save figure, x=Skip to next data record, 0 = Exit): ")
                if user_input in ['n', 'a']:
                    # Add label to labeled remaining_time_intervals df and continue to next time interval and also the temperatue data points in the interval:
                    temperature_data_points = self.assemble_temperatures(interval_temperatures, self.number_of_data_points_required)
                    # create a dataframe with one row, with columns of start, end, and label, and the columns of the time series data points
                    label_value = self.normal_label if user_input == 'n' else self.abnormal_label
                    # Prepare a new row as a map from temperature_data_points interval_loc, interval_start, interval_end, label_value
                    new_map = {**{self.location_col: interval_loc, self.start_col: interval_start, self.end_col: interval_end, self.label_col: label_value},
                               **temperature_data_points}
                    new_row_df = pd.DataFrame(new_map, index=[0]) # create a dataframe with one row, index=[0] must be specified
                    if label_value == self.abnormal_label:
                        self.labeled_abnormal = pd.concat([self.labeled_abnormal, new_row_df])
                    if label_value == self.normal_label:
                        self.labeled_normal = pd.concat([self.labeled_normal, new_row_df])
                    self.previous_label = label_value
                    remaining_temperatures = remaining_temperatures[1:]
                else:
                    self.non_label_action_process(user_input, remaining_temperatures, fig, interval_loc, interval_start, context_before_hrs, context_after_hrs)

        except KeyboardInterrupt:
            pass
        finally:
            self.save_labeled(save_abnormal=True, save_normal=True)
            print(f'{len(self.labeled_normal)} normal labels and {len(self.labeled_abnormal)} abnormal labels saved.')

        if remaining_temperatures.empty:
            print('All remaining_time_intervals labeled!')

        return self.labeled_abnormal, self.labeled_normal

    def assemble_temperatures(self, interval_temperatures, number_of_data_points_required): # added by YS
        '''
        Returns a map of the temperature data points with keys corresponding to the column names expected by the labeled_time_intervals dataframe.
        '''
        # convert a list of tuples to a dictionary:
        a_map = dict(zip(acu.temperature_data_point_colunms(number_of_data_points_required), interval_temperatures[self.temperature_col].tolist()))
        return a_map

    def non_label_action_process(self, user_input, remaining_temperatures, fig, interval_loc, interval_start, context_before_hrs, context_after_hrs):
        # Flip previous label. Only show this option if the user has labeled at least one time interval
        if self.previous_label is not None and (user_input == 'u'):
            yn = ''
            yn = input('This will flip the label of the previous entry i.e. normal -> abnormal, abnormal -> normal (y = Proceed, any other input = Cancel): ')
            if yn == 'y':
                self.flip_labeled()
                print('Label flipped!')
            print()
        # Check progress
        if user_input == 'p':
            progress_str = f'Total abnormal labeled rows: {len(self.labeled_abnormal)} and total normal labeled rows: {len(self.labeled_normal)}, Total unlabeled rows: {len(remaining_temperatures)}'
            print(progress_str)
        # Saving data
        if user_input == 's':
            self.save_labeled(save_abnormal=True, save_normal=True)
        # Saving pyplot figure
        if user_input == 'i':
            try:
                acu.save_fig_interval(fig, self.save_fig_path_full, interval_loc, interval_start, context_before_hrs, context_after_hrs)
            except FileNotFoundError:
                print(f'FileNotFoundError')
                self.save_fig_path_full = input('Unable to save figure. Enter new directory path (absolute or starting ../../data/): ')
                print()
        # Exit routine
        if user_input == '0':
            raise KeyboardInterrupt

    def select_temps(self, start: pd.Timestamp, end: pd.Timestamp): # reviewed by YS
        """
        Select temperatures between the specified start and end times.
        
        :param start: Timestamp representing the start time
        :param end:   Timestamp representing the end time
        :return: Temperatures from the temps DataFrame at the specified location between the specified start and end times.

        Note, this method only works correctly with self.raw_temperatures_df with sorted in increasing order index of type DateTimeIndex.

        """
        return self.raw_temperatures_df.loc[start : end]

    def plot_interval(self, loc: str, start: pd.Timestamp, interval_temperatures: pd.DataFrame, end: pd.Timestamp, 
                      context_before_hrs: float = 2.0, context_after_hrs: float = 2.0,
                      save_fig: object = None): # reviewed by YS
        """
        Plot temperatures within the time interval specified and a given amount of context.
        
        :param loc: Location
        :param start: Timestamp representing the start time
        :param end: Timestamp representing the end time
        :param context_before_hrs: Number of hours before the current time interval to visualize. Defaults to 2.0
        :param context_after_hrs: Number of hours after the current time interval to visualize. Defaults to 2.0
        :param ideal_temp: Ideal temperature. Defaults to 75.0
        :param critical_temp: Critical temperature. Defaults to 90.0
        :param save_fig_path: Path to save temperature visualization to. Defaults to None, so the visualization will not be saved
        
        :return: Figure and Axes objects that make up the plot of the time interval
        """
        df_before   = self.select_temps(start - pd.DateOffset(hours=context_before_hrs), start)  # Raw_Temperatures before the window
        df_interval = interval_temperatures
        df_after    = self.select_temps(end,                                             end + pd.DateOffset(hours=context_after_hrs))  # Temps after the window
        
        # Visualize data
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)
        y_lower_limit = min(self.min_temp, self.ideal_temperature) - 0.5
        y_upper_limit = max(self.max_temp, self.critical_temperature) + 0.5

        ax.set_ylim(y_lower_limit, y_upper_limit)

        interval_enclosed_by_context = pd.concat([df_before, df_interval, df_after]).sort_index().index.drop_duplicates()

        # Plot temperatures and important lines
        temperature_lines_with_idea, = ax.plot(interval_enclosed_by_context,
                                     [self.ideal_temperature] * len(interval_enclosed_by_context),
                                     'g:', linewidth=3, label='Ideal temperature ({}°F)'.format(self.ideal_temperature))
        temperature_lines_with_critical, = ax.plot(interval_enclosed_by_context,
                                                   [self.critical_temperature] * len(interval_enclosed_by_context),
                                                   'r:', linewidth=3, label='Maximum temperature ({}°F)'.format(self.critical_temperature))
        ax.plot(self.temperature_col, 'k',    data=df_interval, linewidth=2)
        ax.plot(self.temperature_col, 'grey', data=df_before,   linewidth=2)
        ax.plot(self.temperature_col, 'grey', data=df_after,    linewidth=2)

        # Highlight time interval
        ax.axvline(start, color='blue', linewidth=0.7)
        ax.axvline(end,   color='blue', linewidth=0.7)
        ax.fill_betweenx(np.arange(self.min_temp - 0.5, self.max_temp + 0.6, 0.1), start, end,
                         color='blue', alpha=0.05)

        ax.set_title('{} {}'.format(loc, start.strftime('%m/%d/%Y %H:%M')), fontsize='xx-large')
        ax.legend(handles=[temperature_lines_with_idea, temperature_lines_with_critical])
        plt.show();
        
        if save_fig is not None:
            acu.save_fig_interval(fig, self.save_fig_path_full,
                              loc, start, context_before_hrs, context_after_hrs)
        return fig, ax


    def save_df_safe(self, df: pd.DataFrame, qualified_base_name):
        """
        Safely save the dataframe
        If the file already exists, increment the suffix to the file name."""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        full_path = self.labeled_dir + qualified_base_name+'-'+timestamp + '.csv.zip'
        df.to_csv(full_path, compression='zip', index=False)
        return full_path

    def save_labeled(self, save_abnormal: bool, save_normal: bool):
        """
        Save all labeled samples, normal or abnormal
        with side effect reset for future labeled collection and disable undo.
        """
        if save_abnormal and len(self.labeled_abnormal) > 0:
            self.save_df_safe(self.labeled_abnormal, self.abonormal_labeled_file_base_name)
            self.labeled_abnormal = self.embpty_labeled_df() # reset the abnormal labeled dataframe for new labeled
            self.previous_label = None # no undo possible
            print('Save abnormal complete!\n')
        if save_normal and len(self.labeled_normal) > 0:
            self.save_df_safe(self.labeled_normal,   self.normal_labeled_file_base_name)
            self.labeled_normal = self.embpty_labeled_df() # reset the normal labeled dataframe for new labeled
            self.previous_label = None # no undo possible
            print('Save normal complete!\n')

    def save_when_enough(self, autosave_freq):
        """
        Save both self.labeled_abnormal or self.labeled_normal when the number of samples in each reaches auto_save_freq
        """
        self.save_labeled(save_abnormal=(len(self.labeled_abnormal) > 0) and (len(self.labeled_abnormal) % autosave_freq == 0),
                          save_normal  =(len(self.labeled_normal) > 0)   and (len(self.labeled_normal) % autosave_freq == 0))

    def embpty_labeled_df(self):
        return pd.DataFrame(columns=acu.temperature_data_point_colunms(self.number_of_data_points_required)+
                            [self.location_col, self.start_col, self.end_col, self.label_col])
