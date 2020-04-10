"""
  This module simplifies the usage of the bokeh library
  by reducing the amount of code to plot a simple figure.
  For example, without this library, to plot a simple line
  with the bokeh library, one must need to::

    from bokeh.palettes import Magma
    from bokeh.layouts import column
    from bokeh.plotting import figure, show
    from bokeh.models import ColumnDataSource
    from bokeh.io import output_notebook, push_notebook

    p = figure( 
        title="Some title",
        plot_width=400,
        plot_height=600)
        
    # Style the figure image
    p.grid.grid_line_alpha = 0.1
    p.xgrid.band_fill_alpha = 0.1
    p.xgrid.band_fill_color = Magma[10][1]
    p.yaxis.axis_label = "Some label for y axis"
    p.xaxis.axis_label = "Some label for x axis"

    # Place the information on plot
    p.line(x_data, y_data,
            legend_label="My legend label",
            line_width=2,
            color=Magma[10][2],
            muted_alpha=0.1,
            line_cap='rounded')
    p.legend.location = "right_top"
    p.legend.click_policy = "disable"

    show(p)

  Wich, with the visual library one might do with 
  just::

    p = visual.line_plot(x_data, y_data,
                        legend_label='My legend label', 
                        title='Some title',
                        y_axis={'label': 'Some label for y axis'},
                        x_axis={'label': 'Some label for x axis'})
    visual.show_plot(p)

  Simple as that... It follows a defualt plotting stily for 
  each plot, presented in the *./utils/configs/plot.yaml*.
  And the user just need to pass the parameters that he
  want to change from this library. It also provides some 
  pre-computation to make more complex graphs, such as box 
  plots, histograms and so on.

  .. note:: 

    This is just a library to simplify most plots used during 
    the notebooks to not populate the algorithm with unecessary
    code... The user can use any library desired to do this same
    plots.

    Also the user can change the *plot.yaml* file to set any default
    plot style that one might want. Please, for that check out the 
    file in *./utils/configs/plot.yaml*.
"""

import os
import logging
from copy import deepcopy
from ruamel.yaml import YAML

import pandas as pd
import numpy as np
from datetime import datetime

from ipywidgets import interact
from bokeh.palettes import Magma
from bokeh.layouts import column
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook, push_notebook


def handle_opts(default, provided):
  """
  Merge the default (set by the plot.yaml file) and 
  user provided plot options into one dictionary.

  :param dict default: The default style guide dict from plot.yaml
  :param dict provided: The user provided properties

  :return: A dict with the merged default and provided plot options
  :rtype: dict
  """
  z = {}
  try:
    overlapping_keys = default.keys() & provided.keys()
    for key in overlapping_keys:
      z[key] = handle_opts(default[key],provided[key])
    for key in default.keys() - overlapping_keys:
      z[key] = deepcopy(default[key])
    for key in provided.keys() - overlapping_keys:
      z[key] = deepcopy(provided[key])
    return z
  except:
    if provided is None:
      return default
    else:
      return provided

output_notebook()
color_theme = Magma[10]

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
plotLog = logging.getLogger("plot_log")

yaml = YAML()
conf_path = '../utils/configs/plot.yaml'
with open(conf_path, 'r') as conf_file:
  def_fig_opts = yaml.load(conf_file)

def line_plot(
    x_data=None,
    y_data=None,
    opts=None,
    **kwargs):
  """
  Create a Bokeh figure object and populate its line 
  propertie with the provided information.

  :param ndarray x_data: The ndarray with x axis values
  :param ndarray y_data: The ndarray with y axis values
  :param dict opts: The desired options of the plot.yaml in dictionary format
  :param kwargs: The desired options of the plot.yaml in directive format

  :return: A Bokeh figure object with the line properties filled
  :rtype: bokeh.Figure
  """
  # Define the figure options
  yopts = dict()
  if opts is not None:
    for opt in opts:
      yopts[opt] = opts[opt]
  if kwargs is not None:
    for opt in kwargs:
      yopts[opt] = kwargs[opt]
  fopts = handle_opts(
    def_fig_opts['line_plot'], yopts)
  # Check axis data
  if x_data is None:
    plotLog.warning("No x axis data was provided...")
  if y_data is None:
    plotLog.error("Please provide y axis data!!")
    return 0
  # Create the figure image
  p = figure(
    title=fopts['title'],
    x_axis_type=fopts['x_axis']['type'],
    y_axis_type=fopts['y_axis']['type'],
    plot_width=fopts['fig_size'][0],
    plot_height=fopts['fig_size'][1])
  # Style the figure image
  p.grid.grid_line_alpha = fopts['dec']['grid']['line_alpha']
  p.xgrid.band_fill_alpha = fopts['dec']['x_grid']['band_alpha']
  p.xgrid.band_fill_color = color_theme[0]
  p.yaxis.axis_label = fopts['y_axis']['label']
  p.xaxis.axis_label = fopts['x_axis']['label']
  # Place the information on plot
  p.line(x_data, y_data,
    legend_label=fopts['legend_label'],
    line_width=fopts['line_width'],
    color=color_theme[fopts['color_index']], 
    muted_alpha=fopts['muted_alpha'],
    line_cap=fopts['line_cap'])
  p.legend.location = fopts['legend']['location']
  p.legend.click_policy = fopts['legend']['click_policy']
  return p


def box_plot(
    score=None,
    labels=None,
    opts=None,
    **kwargs):
  """
  Create a Bokeh figure object and populate its box plot
  propertie with the provided information. To create a 
  box plot, you actually need to combine two segment,
  vbar, and rect object from Bokeh. This method already
  does that for you. It also already computes the 
  statistical median, mean and each quantile.

  :param list score: The list with all values of the distributions
  :param list labels: The list with the group label for each value of score
  :param dict opts: The desired options of the plot.yaml in dictionary format
  :param kwargs: The desired options of the plot.yaml in directive format

  :return: A Bokeh figure object with the line properties filled
  :rtype: bokeh.Figure
  """
  # Define the figure options
  yopts = dict()
  if opts is not None:
    for opt in opts:
      yopts[opt] = opts[opt]
  if kwargs is not None:
    for opt in kwargs:
      yopts[opt] = kwargs[opt]
  fopts = handle_opts(
    def_fig_opts['box_plot'], yopts)
  # Check axis data
  if labels is None:
    plotLog.warning("No labels for x axis data was provided...")
  if score is None:
    plotLog.error("Please provide scores data!!")
    return 0
  # Place the information on plot
  # Create a data frame for the values
  df = pd.DataFrame(dict(score=score, group=labels))
  # Find the quartiles and IQR
  groups = df.groupby('group')
  q1 = groups.quantile(q=0.25)
  q2 = groups.quantile(q=0.5)
  q3 = groups.quantile(q=0.75)
  iqr = q3 - q1
  upper = q3 + 1.5*iqr
  lower = q1 - 1.5*iqr
  # Find the outliers for each category
  def outliers(group):
      cat = group.name
      return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']
  out = groups.apply(outliers).dropna()
  # Prepare outlier data for plotting, 
  # we need coordinates for every outlier
  if not out.empty:
      outx, outy = [], []
      for keys in out.index:
          outx.append(keys[0])
          outy.append(out.loc[keys[0]].loc[keys[1]])
  fopts['x_range'] = df.group.unique()
  # Create the figure image
  p = figure(
    title=fopts['title'],
    x_axis_type=fopts['x_axis']['type'],
    y_axis_type=fopts['y_axis']['type'],
    plot_width=fopts['fig_size'][0],
    plot_height=fopts['fig_size'][1],
    x_range=fopts['x_range'],
    y_range=fopts['y_range'])
  # Style the figure image
  p.grid.grid_line_alpha = fopts['dec']['grid']['line_alpha']
  p.xgrid.band_fill_alpha = fopts['dec']['x_grid']['band_alpha']
  p.xgrid.band_fill_color = color_theme[0]
  p.yaxis.axis_label = fopts['y_axis']['label']
  p.xaxis.axis_label = fopts['x_axis']['label']
  # If no outliers, shrink lengths of stems to be no longer than the minimums or maximums
  qmin, qmax = groups.quantile(q=0.00), groups.quantile(q=1.00)
  upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),upper.score)]
  lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'score']),lower.score)]
  # Stems
  p.segment(fopts['x_range'], upper.score, fopts['x_range'], q3.score, line_color="black")
  p.segment(fopts['x_range'], lower.score, fopts['x_range'], q1.score, line_color="black")
  # Boxes
  p.vbar(fopts['x_range'], 0.7, q2.score, q3.score, fill_color=color_theme[2], line_color="black")
  p.vbar(fopts['x_range'], 0.7, q1.score, q2.score, fill_color=color_theme[8], line_color="black")
  # Whiskers (almost-0 height rects simpler than segments)
  p.rect(fopts['x_range'], lower.score, 0.001, 0.005, line_color="black")
  p.rect(fopts['x_range'], upper.score, 0.001, 0.005, line_color="black")
  # Outliers
  if not out.empty:
    p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
  return p

def hist_plot(
    hist=None,
    edges=None,
    opts=None,
    **kwargs):
  """
  Create a Bokeh figure object and populate its histogram 
  plot propertie with the provided information. To create a 
  histogram plot, you actually need to the correct properties
  of the quad object from Bokeh. This method already does that 
  for you. It also already computes the correct values, and 
  create the bins correctly.

  :param ndarray hist: The hist output from numpy.histogram
  :param ndarray edges: The histogram edges output from numpy.histogram
  :param dict opts: The desired options of the plot.yaml in dictionary format
  :param kwargs: The desired options of the plot.yaml in directive format

  :return: A Bokeh figure object with the line properties filled
  :rtype: bokeh.Figure
  """
  # Define the figure options
  yopts = dict()
  if opts is not None:
    for opt in opts:
      yopts[opt] = opts[opt]
  if kwargs is not None:
    for opt in kwargs:
      yopts[opt] = kwargs[opt]
  fopts = handle_opts(
    def_fig_opts['histogram_plot'], yopts)
  # Check axis data
  if hist is None:
    plotLog.error("Please provide the proper hist parameter.")
    return 0
  if edges is None:
    plotLog.error("Please provide the proper edges parameter.")
    return 0
  # Create the figure image
  p = figure(
    title=fopts['title'],
    x_axis_type=fopts['x_axis']['type'],
    y_axis_type=fopts['y_axis']['type'],
    plot_width=fopts['fig_size'][0],
    plot_height=fopts['fig_size'][1])
  # Style the figure image
  p.grid.grid_line_alpha = fopts['dec']['grid']['line_alpha']
  p.xgrid.band_fill_alpha = fopts['dec']['x_grid']['band_alpha']
  p.xgrid.band_fill_color = color_theme[0]
  p.yaxis.axis_label = fopts['y_axis']['label']
  p.xaxis.axis_label = fopts['x_axis']['label']
  # Place the information on plot
  p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
    fill_color=color_theme[fopts['color_index']], line_color="white", alpha=0.5)
  return p

def multline_plot(
    x_data=None,
    y_data=None,
    opts=None,
    **kwargs):
  """
  Create a Bokeh figure object and populate a line object
  of the bokeh library for each line data provided in the 
  y_data list parameter of this function.

  :param list x_data: The list with a ndarray data for the x axis of each line
  :param list y_data: The list with a ndarray data for the y axis of each line
  :param dict opts: The desired options of the plot.yaml in dictionary format
  :param kwargs: The desired options of the plot.yaml in directive format

  :return: A Bokeh figure object with the line properties filled
  :rtype: bokeh.Figure
  """
  # Define the figure options
  yopts = dict()
  if opts is not None:
    for opt in opts:
      yopts[opt] = opts[opt]
  if kwargs is not None:
    for opt in kwargs:
      yopts[opt] = kwargs[opt]
  fopts = handle_opts(
    def_fig_opts['line_plot'], yopts)
  # Check axis data
  if x_data is None:
    plotLog.warning("No x axis data was provided...")
  if y_data is None:
    plotLog.error("Please provide y axis data!!")
    return 0
  # Create the figure image
  p = figure(
    title=fopts['title'],
    x_axis_type=fopts['x_axis']['type'],
    y_axis_type=fopts['y_axis']['type'],
    plot_width=fopts['fig_size'][0],
    plot_height=fopts['fig_size'][1])
  # Style the figure image
  p.grid.grid_line_alpha = fopts['dec']['grid']['line_alpha']
  p.xgrid.band_fill_alpha = fopts['dec']['x_grid']['band_alpha']
  p.xgrid.band_fill_color = color_theme[0]
  p.yaxis.axis_label = fopts['y_axis']['label']
  p.xaxis.axis_label = fopts['x_axis']['label']
  # Place the information on plot
  data, ind_track = x_data, 0
  if type(x_data) is not list:
    x_data = list()
    for k in range(len(y_data)):
      x_data.append(data)
  for x, y in zip(x_data, y_data):
    p.line(x, y,
      legend_label=fopts['legend_label'][ind_track],
      line_width=fopts['line_width'],
      color=color_theme[fopts['color_index'][ind_track]], 
      muted_alpha=fopts['muted_alpha'],
      line_cap=fopts['line_cap'])
    ind_track += 1
  p.legend.location = fopts['legend']['location']
  p.legend.click_policy = fopts['legend']['click_policy']
  return p


def show_plot(*args):
  """
  This function shows the figures provided as arguments
  by default, in a column manner.

  :param args: The bokeh.Figure objects to be show in a figure
  """
  if args is not None:
    show(column(*args))
  else:
    plotLog.error("No plot was provided!!")
