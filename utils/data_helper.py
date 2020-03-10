import os
import logging

import astropy as ast
from astropy.table import Table

from .data_struc import curve

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class reader:
    """
    """
    def __init__(self):
        self.log = logging.getLogger("reader_log")
        self.log.info("Reader module created...")
    
    def from_txt(self):
        pass
    
    def from_file(
            self,
            path=None,
            label=None,
            index=None,
            feature=None ):
        """
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
        return curve(hdu=hdu_data, label=label, index=index)

    def list_features(
            self,
            folders=None ):
        """
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


    def from_folder(
            self,
            folder=None,
            label=None,
            index=None ):
        """
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
                curve(hdu=hdu_data, label=label, index=index) )
        return curves
