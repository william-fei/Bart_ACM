#!/usr/bin/env python3
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: ac-monitor
#     language: python
#     name: ac-monitor
# ---

# %% [markdown]
# # Training Example Creation
# This is the program to perform labeling examples for supervised learning for
# the anomality detection of Airconditioner.
# %% [markdown]
# It is extracted from the original program ./AC_labler.py for the purest behavior of training example creation.
# With this program, the original program will be osbsolete.
#
# *Author*: Steven Yuan
#
# *Project lead*: Yu Shen
#
# ## Import packages

# %%
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

# from IPython.display import clear_output
#from tqdm import tqdm

from importlib import reload

# %% [markdown]
# aclabeler is a package that contains the functions to label the data.
# It defines a class called `ACLabeler` that contains the functions to label the data.
#
# %%
import sys
sys.path.insert(0, '../scripts') # for aclabeler.py moved to src/scripts

import aclabeler

# %% [markdown]
# ## Configurations
# %%
root_data_dir = '../../data/'  # The root directory for the data. All the paths are relative to this directory.
raw_temperatures_name = 'raw/indoor-temp-20220601-0912-ACELS_C40.csv.zip'  # File containing the RAW temperature data
# time_intervals = 'intervals/timewindows_4H_rs2022'  # File containing the definitions of the time intervals to create the time series data with labels
labeled_base_name = 'yaqian_tang_C40'  # File to output the labels for the time windows defined in the time_intervals

# be careful the value of labeled_time_intervals points to the results of labeling. If using the same value,
# I'm not sure if it will have the correct append behavor or just overwriting the existing labeling results!

autosave_freq = 20  # Number of labels before automatically saving
save_fig_path = 'images/labeling_samples/'  # Path to save images generated by the labeling program


# %% [markdown]
# ## Create object labeler
#
# %% [markdown]
# The constructor ACLabeler takes a long time to execute. It might be optimized.

# %%
reload(aclabeler)
from aclabeler import ACLabeler

# %%
labeler = ACLabeler(
    root_data_dir         =root_data_dir,
    raw_temperatures_name =raw_temperatures_name,
    labeled_base_name      =labeled_base_name,
    save_fig_path=save_fig_path
    )

# %% [markdown]
# ## Perform labeling by launching the interactive labeling function: labeler.label
# %%

# %%

# %%
context_before_hrs = 4  # Number of hours to plot before current time window as context
context_after_hrs = 4  # Number of hours to plot before current time window as context
lab = labeler.label(autosave_freq         =autosave_freq,
                    context_before_hrs    =context_before_hrs,
                    context_after_hrs     =context_after_hrs,
                    show_abnormality_score=False,
                    start_time            ='2022-09-09T08:07:01.000-0700'
                   )
# %%
