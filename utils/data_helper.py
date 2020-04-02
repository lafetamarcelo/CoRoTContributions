"""
    
    This module is responsible to read the *.fits* files and return the 
    readed data as a :py:class:`Curve <utils.data_struc.Curve>` objects, 
    which is a more suitable format to read the data. Or one might choose 
    to only receive the  data in a simple type as possible such as lists 
    and dictionaries, thus by chosing this method, one will loose the 
    hability to use the inherited computing pre processing features from 
    the :py:class:`Curve <utils.data_struc.Curve>` format.
"""

import os
import logging
import astropy as ast
from astropy.table import Table
from .data_struc import Curve

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class Reader:
    """
    The reader module is responsible for reading the raw *.fits* files
    and provide the data in a more friendly data structure for the python
    environment. It supports both unique *.fits* files such as a batch
    processing approach, using folders filled with several *.fits* files.

    As simple as it is to call a class, the reader package has no usage
    complication. For one to import and use it's methods, it is only 
    necessary to do like this::

        import utils.data_helper as dh
        myReader = dh.Reader()

    .. admonition:: Retrieved data structure

        One must understand that the retrieved data will be or 
        :py:class:`Curve <utils.data_struc.Curve>` objects or 
        they will be composed of simple ``list`` and ``dict`` outputs.
        All methods have a particular parameter, with default 
        ``simple_out=False`` thence returning the data as 
        :py:class:`Curve <utils.data_struc.Curve>`. If one defines the 
        parameter ``simple_out=True``, one will receive the obtained data 
        as dictionaries of indexed curves in lists, wich is not advised.
    
    .. versionadded:: 0.1
        The `from_file` and `from_folder` methods where added.
    """

    def __init__(self):
        self.log = logging.getLogger("reader_log")
        self.log.info("Reader module created...")
    
    def from_txt(self):
        pass

    def list_features(
            self,
            folders=None ):
        """
        Get only the features list, for each *.fits* curve file,
        inside the folders list.

        :param list folders: Paths to the folders with the *.fits*
        :return: The list with features available for each *.fits* found
        :rtype: list
        """
        if folders is None:
            self.log.info("Please provide the folder path:")
            folders = input()
        curves = list()
        for folder in folders:
            folder = os.path.abspath(folder)
            files = os.listdir(folder)
            for file in files:
                curve = { "label": folder, "attr": list() }
                hdu_data = ast.io.fits.open( os.path.join(folder, file), memmap=True )
                for index in [1,2,3]:
                    raw_table = Table.read(hdu_data[index], memmap=True)
                    curve["attr"].append( raw_table.colnames )
                curves.append( curve )
        return curves

    def from_file(
            self,
            path=None,
            label=None,
            index=None,
            feature=None ):
        """
        Get the white light curve from the provided *.fits* file, and
        label this curve with the provided label (or with the folder
        name, if `label=None`) and return the data_sctruc.Curve.

        :param str path: Paths to the desired *.fits* file
        :param str label: The label for the returned curve
        :param int index: The HUD table index
        :param str feature: The light curve specific feature name

        :return: The specific feature of light curve in more suitable format
        :rtype: data_struc.Curve
        """
        if path is None:
            self.log.info("Please provide the file path:")
            path = input()
        path = os.path.abspath(path)
        if label is None:
            label = path.split(os.sep)[-3]
            self.log.info("No custom label was provided!")
            self.log.info("Setting label as:" + label)
        hdu_data = ast.io.fits.open( path, memmap=True )
        return Curve(hdu=hdu_data, label=label, index=index)

    def from_folder(
            self,
            folder=None,
            label=None,
            index=None ):
        """
        Get the white light curve of each *.fits* file presented inside 
        the provided folder, label each one or with the provided label, 
        or with the folder name, and return a list with one data_struc.Curve
        variable for each *.fits* file.

        :param str folder: Paths to the folder with the *.fits* files
        :param str label: The label for the returned light curves
        :param int index: The HUD table index
        
        :return: A list of data_struc.Curve
        :rtype: list
        """
        if folder is None:
            self.log.info("Please provide the folder path:")
            folder = input()
        folder = os.path.abspath(folder)
        if label is None:
            label = folder.split(os.sep)[-2]
            self.log.info("No custom label was provided!")
            self.log.info("Setting label as:" + label)
        files, curves = os.listdir(folder), list()
        self.log.info("Reading {} curve packages...".format(len(files)))
        for file_name in files:
            hdu_data = ast.io.fits.open( os.path.join(folder, file_name), memmap=True )
            curves.append( 
                Curve(hdu=hdu_data, label=label, index=index) )
        return curves
