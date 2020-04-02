"""
    
    This module gathers all the custom data 
    structures created to replace the *.fits*
    format provided by the 
"""

import os
import julian
import logging
import pandas as pd
import astropy as ast
import datetime as dt
from astropy.table import Table
from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt

register_matplotlib_converters()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

try:
    from jupyterthemes import jtplot
    jtplot.style(
        figsize=(16,8),
        ticks=True,
        context='talk', 
        fscale=0.6, 
        spines=False, 
        gridlines='--')
except:
    pass


class Curve:
    """
        The ligth curve object.
    """
    
    def __repr__(
            self ):
        return "Light Curve Object -- based {}".format(self.from_file)
    
    def __init__(
            self,
            hdu=None,
            index=None,
            label=None ):
        self.status = { "indexed": False }
        self.log = logging.getLogger("curve_log")
        if label is None:
            label = "Empty"
            self.log.warning("This curve has no label...")
            self.log.warning("Curve label set to: {}".format(label))
        self.labeler = label
        index = 3 if index is None else index + 1
        if hdu is not None:
            self.from_file = "HDU"
            self.raw_table = Table.read(hdu[index], memmap=True).to_pandas()
            self.feature_list = self.raw_table.keys()
            self.julian_to_stdtime()
    
    def __getitem__(
            self, 
            feature=None ):
        if feature is None:
            self.log.warning("Please provide a valid feature value, please select one from")
            self.log.warning(self.feature_list); pass
        return self.raw_table[feature].to_list()
    
    def index_tables(
            self,
            index=None ):
        """
        """
        index = 2 if index is None else index
        self.raw_table = self.raw_table[index].to_pandas()
        self.feature_list = self.feature_list[index]
        self.status["indexed"] = True
        self.julian_to_stdtime()
    
    def julian_to_stdtime(
            self ):
        """
        """
        ref_time = [ julian.from_jd(date, fmt="mjd") for date in self.raw_table["DATEBARTT"].to_list() ]
        date_frame = pd.DataFrame(data=ref_time, columns=["DATE"])
        self.raw_table = pd.concat([self.raw_table, date_frame], axis=1, sort=False)
        self.feature_list = self.raw_table.keys()
    
    def show_feature(
            self,
            feature=None ):
        """
        """
        if feature is None:
            self.log.error("No feature value provided.")
        plt.figure(figsize=(6,4))
        plt.plot(self.__getitem__("DATE"), self.__getitem__(feature), lw=2.5)
        plt.show()