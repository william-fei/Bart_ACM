import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import clear_output

class ACLabeler:
    """
    Labeler for BART server location temperature data, for use with Jupyter.
    """

    def __init__(self, path: str, windows: str, labeled: str, temps: str,
                 dt_col: str = 'timedt', temp_col: str = 'temp', location_column_name: str = 'loc', start_col: str = 'start', end_col: str = 'end', label_col: str = 'ab'):
        """
        Initialize parameters for labeler.

        :param path: Path containing data
        :param windows: File containing time windows
        :param labeled: File containing labeled time windows
        :param temps: File containing temperature data
        :param dt_col: Column containing timestamps in the temps df
        :param temp_col: Column containing temperatures in the temps df
        :param location_column_name: Column containing locations in the windows, labeled, and temps dfs
        :param start_col: Column containing start times for each time window in the windows and labeled dfs
        :param end_col: Column containing end times for each time window in the windows and labeled dfs
        :param label_col: Column containing labels for each time window in the labeled df
        """
        self.path = path
        self.windows = windows
        self.labeled = labeled
        self.temps = temps
        
        self.windows_zip = path + windows + '.zip'
        self.labeled_zip = path + labeled + '.zip'
        self.labeled_csv = path + labeled + '.csv'

        self.dt_col = dt_col
        self.temp_col = temp_col
        self.location_column_name = location_column_name
        self.start_col = start_col
        self.end_col = end_col
        self.label_col = label_col

        # Preload temperature data
        try:
            self.temperature_df = pd.read_csv(
                path + temps + '.zip',
                index_col=dt_col,
                converters={dt_col: pd.to_datetime}
            )
            
            # Important temperature values
            self.min_temp = min(self.temperature_df[self.temp_col])
            self.max_temp = max(self.temperature_df[self.temp_col])
        except FileNotFoundError:
            print('Unable to load temperature data, created empty temperature DataFrame')
            self.temperature_df = pd.DataFrame(index=pd.Index([], name=dt_col),columns=[temp_col])
            self.min_temp = 0.0
            self.max_temp = 0.0

    def label(self,
              normal_label: object = 0, abnormal_label: object = 1,
              autosave_freq: int = 10, 
              context_before_hrs: float = 2.0, context_after_hrs: float = 2.0, 
              ideal_temp: float = 75.0, crit_temp: float = 90.0,
              show_score: bool = True,
              window_len: int = 0,
              savefig_path: str = ''
              ):
        """
        Main labeling routine. For every time window not yet labeled, visualize the temperature data in that time window
        and prompt the user to label the data

        :param normal_label: Label for normal time windows. Defaults to 0
        :param abnormal_label: Label for abnormal time windows. Defaults to 1
        :param context_before_hrs: Number of hours before the current time window to visualize. Defaults to 2.0
        :param context_after_hrs: Number of hours after the current time window to visualize. Defaults to 2.0
        :param ideal_temp: Ideal temperature, for visualization purposes. Defaults to 75.0
        :param crit_temp: Critical temperature - temperatures above this value indicate a potential AC failure - for visualization and abnormality score calculation purposes. Defaults to 90.0
        :param show_score: Show "abnormality score" (see comments in function). Defaults to True
        :param window_len: If positive, require this many temperature data points in each time window. Defaults to 0
        :param autosave_freq: Automatically save after this many labelings. Defaults to 10
        :param savefig_path: Path to save temperature visualizations to. Defaults to current directory

        :return: Labeled windows DataFrame
        """
        # Load time window data
        windows = self.read_windows()
        try:
            labeled = self.read_labeled()
        except FileNotFoundError:
            labeled = pd.DataFrame(columns=[self.location_column_name, self.start_col, self.end_col, self.label_col])

        # Start at next unlabeled window
        if not labeled.empty:
            r = labeled.iloc[-1]
            i = windows[lambda df: (df[self.location_column_name] == r[self.location_column_name]) & (df[self.start_col] == r[self.start_col])].iloc[0].name
            windows = windows.iloc[(i + 1):]
        
        num_labeled = 0  # Number of time windows labeled in the current session

        sns.set_theme()  # Set pyplot theme

        try:
            while not windows.empty:
                clear_output(wait=True)  # Clear previous output

                # Autosave
                if (num_labeled != 0) and (num_labeled % autosave_freq == 0):
                    self.save_labeled(labeled)

                # Select temperatures in the time window
                row = windows.iloc[0]
                row_loc = row[self.location_column_name]
                window_start = row[self.start_col]
                window_end = row[self.end_col]
                
                df_window = self.select_temps(row_loc, window_start, window_end).iloc[:-1]
                
                # Do not label time windows that do not contain the right number of data points
                if (window_len > 0) and (len(df_window.index) != window_len):
                    windows = windows.iloc[1:]
                    continue
                    
                # Plot temperature curve
                fig, ax = self.plot_timewindow(row_loc, window_start, window_end,
                                               context_before_hrs=context_before_hrs, context_after_hrs=context_after_hrs,
                                               ideal_temp=ideal_temp, crit_temp=crit_temp);
                
                # Calculate "abnormality score": the sum of the square of the difference between the max temp and
                # every temperature above the max temp. Idea taken from Floyd Fang
                if show_score:
                    ab_score = sum(max((temp - crit_temp), 0)**2 for temp in df_window.iloc[:-1][self.temp_col])
                    print('Abnormality score: {:.2f}\n'.format(ab_score))

                ans = ''  # User input

                # Prompting for user input
                while ans not in ['n', 'a']:
                    ans = input('Enter label (n = Label normal, a = Label abnormal, {}p = Check progress, s = Save labels, i = Save figure, 0 = Exit): '.format('u = Flip previous label, ' if num_labeled > 0 else ''))

                    # Flip previous label. Only show this option if the user has labeled at least one time window
                    if (num_labeled > 0) and (ans == 'u'):
                        yn = ''
                        yn = input('This will flip the label of the previous entry i.e. normal -> abnormal, abnormal -> normal (y = Proceed, any other input = Cancel): ')
                        
                        if yn == 'y':
                            prev_label = labeled.at[len(labeled.index) - 1, self.label_col]
                            labeled.at[len(labeled.index) - 1, self.label_col] = normal_label if (prev_label == abnormal_label) else abnormal_label
                            print('Label flipped!')
                            
                        print()
                            
                    # Check progress
                    if ans == 'p':
                        print('Total labels: {}\t\tCurrent labels: {}\t\tTotal unlabeled: {}\n'.format(len(labeled.index), num_labeled, len(windows.index)))
                            
                    # Saving data
                    if ans == 's':
                        self.save_labeled(labeled)
                        print('Save complete!\n')

                    # Saving pyplot figure
                    if ans == 'i':
                        try:
                            self.savefig_timewindow(fig, savefig_path, row_loc, window_start, context_before_hrs, context_after_hrs)
                        except FileNotFoundError:
                            savefig_path = input('Unable to save figure. Enter new directory path: ')
                            print()
                    
                    # Exit routine
                    if ans == '0':
                        raise KeyboardInterrupt

                # Add label to labeled windows df and continue to next time window
                labeled = pd.concat([labeled, windows.iloc[[0]].assign(**{self.label_col: normal_label if ans == 'n' else abnormal_label})])
                windows = windows[1:]
                num_labeled += 1
        except KeyboardInterrupt:
            pass
        finally:
            self.save_labeled(labeled)
            print('{} labels saved, exited labeling\n'.format(num_labeled))

        if windows.empty:
            print('All time windows labeled!')

        return labeled
    
    
    def select_temps(self, location: str, start: pd.Timestamp, end: pd.Timestamp):
        """
        Select temperatures at the specified location between the specified start and end times.
        
        :param location: Location
        :param start: Timestamp representing the start time
        :param end: Timestamp representing the end time
        :return: Temperatures from the temps DataFrame at the specified location between the specified start and end times
        """
        #return self.temperature_df.query('{} == "{}"'.format(self.location_column_name, location)) \
        # Use a more efficient method of selecting rows with the expected location and time range, with the timestamp as the index
        return self.temperature_df[self.temperature_df[self.location_column_name] == location] \
                .drop(columns=self.location_column_name) \
                .sort_index() \
                .loc[start : end]

    def plot_timewindow(self, loc: str, start: pd.Timestamp, end: pd.Timestamp, 
                        context_before_hrs: float = 2.0, context_after_hrs: float = 2.0, 
                        ideal_temp: float = 75.0, crit_temp: float = 90.0,
                        savefig_path: str = None):
        """
        Plot temperatures within the time window specified and a given amount of context.
        
        :param loc: Location
        :param start: Timestamp representing the start time
        :param end: Timestamp representing the end time
        :param context_before_hrs: Number of hours before the current time window to visualize. Defaults to 2.0
        :param context_after_hrs: Number of hours after the current time window to visualize. Defaults to 2.0
        :param ideal_temp: Ideal temperature. Defaults to 75.0
        :param crit_temp: Critical temperature. Defaults to 90.0
        :param savefig_path: Path to save temperature visualization to. Defaults to None, so the visualization will not be saved
        
        :return: Figure and Axes objects that make up the plot of the time window
        """
        df_window = self.select_temps(loc, start, end)
        df_before = self.select_temps(loc, start - pd.DateOffset(hours=context_before_hrs), start)  # Temps before the window
        df_after = self.select_temps(loc, end, end + pd.DateOffset(hours=context_after_hrs))  # Temps after the window
        
        # Visualize data
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)
        ax.set_ylim(self.min_temp - 0.5, self.max_temp + 0.5)

        x = pd.concat([df_before, df_window, df_after]).sort_index().index.drop_duplicates()

        # Plot temperatures and important lines
        ideal, = ax.plot(x, [ideal_temp] * len(x), 'g:', linewidth=3, label='Ideal temperature ({}°F)'.format(ideal_temp))
        crit, = ax.plot(x, [crit_temp] * len(x), 'r:', linewidth=3, label='Maximum temperature ({}°F)'.format(crit_temp))
        ax.plot(self.temp_col, 'k', data=df_window, linewidth=2)
        ax.plot(self.temp_col, 'grey', data=df_before, linewidth=2)
        ax.plot(self.temp_col, 'grey', data=df_after, linewidth=2)

        # Highlight time window
        ax.axvline(start, color='blue', linewidth=0.7)
        ax.axvline(end, color='blue', linewidth=0.7)
        ax.fill_betweenx(np.arange(self.min_temp - 0.5, self.max_temp + 0.6, 0.1), start, end,
                         color='blue', alpha=0.05)

        ax.set_title('{} {}'.format(loc, start.strftime('%m/%d/%Y %H:%M')), fontsize='xx-large')
        ax.legend(handles=[ideal, crit])
        plt.show();
        
        if savefig_path is not None: 
            try:
                self.savefig_timewindow(fig, savefig_path, loc, start, context_before_hrs, context_after_hrs)
            except FileNotFoundError:
                print('Unable to save figure')
                
        return fig, ax
    
    
    @staticmethod
    def savefig_timewindow(fig: Figure, savefig_path: str,
                           loc: str, start: pd.Timestamp, context_before_hrs: float, context_after_hrs: float):
        """
        Attempts to save a matplotlib figure depicting a temperature curve. Throws a FileNotFoundError if the path cannot be found.
        
        :param fig: The Figure object to be saved
        :param savefig_path: Path to save figure in
        :param loc: Location
        :param start: Timestamp representing the start time
        :param context_before_hrs: Number of hours before the current time window to visualize
        :param context_after_hrs: Number of hours after the current time window to visualize
        """
        fig.savefig('{}{}-{}-b{}-a{}.png'.format(savefig_path, loc, start.strftime('%m%d%Y-%H%M'), context_before_hrs, context_after_hrs), format='png')
        print('Figure saved!\n')
        
    
    def read_windows(self):
        """
        Read unlabeled windows data.
        
        :return: pandas DataFrame containing the data in self.windows_zip
        """
        return pd.read_csv(self.windows_zip, converters={self.start_col: pd.to_datetime, self.end_col: pd.to_datetime})
    
    
    def read_labeled(self):
        """
        Read labeled data.
        
        :return: pandas DataFrame containing the data in self.labeled_zip
        """
        return pd.read_csv(self.labeled_zip, converters={self.start_col: pd.to_datetime, self.end_col: pd.to_datetime})
    
    
    @staticmethod
    def save_df(df: pd.DataFrame, name: str, archive_name: str):
        """
        Saves a DataFrame in a zipped csv file.
        
        :param df: Any DataFrame
        :param name: Name of the zip file. Make sure to include a .zip extension!
        :param archive_name: Name of the csv file. Name sure to include a .csv extension!
        
        :return: The inputted DataFrame
        """
        df.to_csv(name, index=False, compression=dict(method='zip', archive_name=archive_name))
        return df
    
    
    def save_labeled(self, df: pd.DataFrame):
        """
        Save labeled data.
        
        :param df: DataFrame containing labeled time windows
        
        :return: The inputted DataFrame
        """
        return self.save_df(df, self.labeled_zip, self.labeled_csv)
    
    
    def set_windows(self, windows: str):
        """
        Set time windows input file name.
        
        :param windows: File containing time windows
        """
        self.windows = windows
        self.windows_zip = self.path + windows + '.zip'
        self.windows_csv = self.path + windows + '.csv'
        
        
    def set_labeled(self, labeled: str):
        """
        Set labeled time windows output file name.
        
        :param labeled: File containing labeled time windows
        """
        self.labeled = labeled
        self.labeled_zip = self.path + labeled + '.zip'
        self.labeled_csv = self.path + labeled + '.csv'
        
    
    def set_temps(self, temps: str, reload_temps: bool = False):
        """
        Set temperature data file name.
        
        :param temps: File containing temperature data
        :param reload_temps: Whether to reload the temperature file or not. Defaults to False
        """
        self.temps = temps
        
        if reload_temps:
            try:
                self.temperature_df = pd.read_csv(
                    self.path + temps + '.zip',
                    index_col=self.dt_col,
                    converters={self.dt_col: pd.to_datetime}
                )
            except FileNotFoundError:
                print('Unable to load temperature data, created empty temperature DataFrame')
                self.temperature_df = pd.DataFrame(index=pd.Index([], name=self.dt_col),columns=[self.temp_col])
                
    
    def set_path(self, path: str, reload_temps: bool = False):
        """
        Set path/directory containing data files.
        
        :param path: Path containing data
        :bool reload_temps: Whether to reload the temperature file or not. Defaults to False
        """
        self.path = path
        
        self.set_windows(self.windows)
        self.set_labeled(self.labeled)
        self.set_temps(self.temps, reload_temps=reload_temps)
