# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
# ---

# %% [markdown]
# # Notebook template

# %% [markdown]
# <!-- Every notebook should at least have a summary of its purpose -->
# **Purpose of this notebook**\
# A basic summary of what this notebook aims to achieve.
# <!-- Additional sections. Uncomment as needed. -->
#
# <!-- **Useful links**
# - [link_1](https:www.example.com)
# - [link_2](https:www.example.com) -->
#
# <!-- **Conclusions and next steps**\
# A summary of what is achieved in this notebook and what the follow up should be. -->

# %%
# Imports
import pathlib

# Automatically reload modules before executing Python code
# %reload_ext autoreload
# %autoreload 2

# Set directories
root_dir = pathlib.Path().resolve().parent
data_dir = root_dir / "data"
