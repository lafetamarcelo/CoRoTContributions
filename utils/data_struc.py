import os
import logging
import datetime
import pandas as pd
import astropy as ast
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
        theme='onedork', 
        context='talk', 
        fscale=1.4, 
        spines=False, 
        gridlines='--')
except:
    pass


class curve:
    """
        The ligth curve object.
    """

    def __repr__(
            self ):
        return "Light Curve Object -- based {}".format(self.from_file)

    def __init__(
            self,
            hdu=None,
            hdu_featured=None,
            label=None ):
        self.log = logging.getLogger("curve_log")
        if label is None:
            label = "Empty"
            self.log.warning("This curve has no label...")
            self.log.warning("Curve label set to: {}".format(label))
        self.labeler = label
        if hdu is not None:
            self.from_file = "HDU"
            self.raw_tables = [ Table.read(item, memmap=True) for item in hdu[1:] ]
            self.feature_list = [ table.keys() for table in self.raw_tables ]
        if hdu_featured is not None:
            feature = hdu_featured[0].upper()


    def get_feature(
            self,
            feature=None ):
        if feature is None:
            self.log.error("No feature value provided.")
        feature = feature.upper()
        query_data, time_data = list(), list()
        for group in self.feature_list:
            if feature in group:
                index = self.feature_list.index(group)
                table = self.raw_tables[index].to_pandas()
                query_data.append(table[feature].to_list())
                time_data.append(table["DATEBARTT"].to_list())
        return { "time" : time_data, "data" : query_data }

    def show_feature(
            self,
            feature=None ):
        if feature is None:
            self.log.error("No feature value provided.")
        values = self.get_feature(feature=feature)
        plt.figure(figsize=(8,6))
        for y, time in zip(values["data"], values["time"]):
            plt.plot(time, y, lw=3)
        plt.show()

    def julian_to_stdtime(
            self,
            time=None ):
        if time is None:
            self.log.error("Please provide a proper time vector.")
        ref_time = datetime.datetime.strptime(time, "%y%j").date()
        return ref_time.strftime("%d/%m/%Y")
