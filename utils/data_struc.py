"""
    
    This module gathers all the custom data 
    structures created to replace the *.fits*
    format provided by the raw data-set. 

    It represents the direct interface from the
    complex representation of the astropy.table
    modules, to simple `array` python variables.
"""

import os
import julian
import logging
import pandas as pd
import astropy as ast
import datetime as dt
from astropy.table import Table
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class Curve:
    """
        This object maintain the light curve HUD table,
        and represents an interface to get data from the
        HUD tables of the astropy library and the python
        environment. Therefore, it just represent a simple
        interface to transcript the HUD table informations
        to simple python variables such as `dict`, `list` 
        and `array`.

        For example to get create and extract the data 
        from a curve object the user just need to::

            import utils.data_struc as ds
            curve = ds.Curve(hdu=hduTable, index=hduTableIndex, label=curveLabel)
            feature = curve['FEATURE NAME']
        
        By using the :py:class:`Reader <utils.data_helper.Reader>`
        this is even more transparent. Here you need to provide

        :param astronomy.table.Table hdu: The HDU table from astronomy library
        :param int index: The desired HDU table index to be used
        :param str label: The desired label for this light curve

        And then, by just argumenting the column name of the 
        table, the user can get the values of the column as a 
        ndarray variable.

        .. admonition:: Advantages

            One must question why use this particular structure 
            instead of just using the astropy.table.Table 
            objects. But, since in most time we just use the last
            HDU table (usually `index=2`), this structure automatically
            removed all other tables and just save the desired one
            in a memory map format (that has a better performance).

            This approach is memory efficient because, the information
            removed is usually something close to 10 times bigger than 
            the used one... that is, the first and second table are 
            at least ten times bigger than the third table (wich is 
            the most used one, `index=2`). Therefore, for this application, 
            this approach is actually efficient when compared to just 
            loading the data and dealing with the information in 
            astropy tables.

        .. versionadded:: 0.1
            The `from_file` and `from_folder` methods where added.
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
        Handly index the HDU table from the Curve object,
        by replacing the raw_table variable with only the
        desired HDU table.
        
        :param int index: The index of the desired HDU table
        """
        index = 2 if index is None else index
        self.raw_table = self.raw_table[index].to_pandas()
        self.feature_list = self.feature_list[index]
        self.status["indexed"] = True
        self.julian_to_stdtime()
    
    def julian_to_stdtime(
            self ):
        """
        Change the julian date variable of the HDU tables
        to standard time representations.
        """
        ref_time = [ julian.from_jd(date, fmt="mjd") for date in self.raw_table["DATEBARTT"].to_list() ]
        date_frame = pd.DataFrame(data=ref_time, columns=["DATE"])
        self.raw_table = pd.concat([self.raw_table, date_frame], axis=1, sort=False)
        self.feature_list = self.raw_table.keys()