#!/usr/local/bin/python
# encoding: utf-8
"""
milliquas.py
============
:Summary:
    Import Milliquas catagloue from plain text file

:Author:
    David Young

:Date Created:
    August 25, 2015

:dryx syntax:
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script/module please email me: d.r.young@qub.ac.uk

:Tasks:
    @review: when complete pull all general functions and classes into dryxPython

# xdocopt-usage-tempx
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import codecs
import string

import re
from docopt import docopt
from dryxPython import mysql as dms
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
# from ..__init__ import *


class milliquas():

    """
    The worker class for the milliquas module

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``pathToDataFIle`` -- path to the milliquas data file
        - ``version`` -- version of the milliquas catalogue


    **Todo**
        - @review: when complete, clean milliquas class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            settings=False,
            pathToDataFile=False,
            version=""
    ):
        self.log = log
        log.debug("instansiating a new 'milliquas' object")
        self.settings = settings
        self.pathToDataFile = pathToDataFile
        self.version = version

        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # INITIAL ACTIONS
        # SETUP DATABASE CONNECTIONS
        from sherlock import database
        db = database(
            log=self.log,
            settings=self.settings
        )
        self.transientsDbConn, self.cataloguesDbConn = db.get()

        pathToReadFile = pathToDataFile
        try:
            self.log.debug("attempting to open the file %s" %
                           (pathToReadFile,))
            readFile = codecs.open(pathToReadFile, mode='r')
            self.mqData = readFile.read()
            readFile.close()
        except IOError, e:
            message = 'could not open the file %s' % (pathToReadFile,)
            self.log.critical(message)
            raise IOError(message)

        readFile.close()

        self.dbTableName = "tcs_cat_milliquas_v" + \
            self.version.replace(" ", "").replace("v", "").replace(".", "_")

        return None

    def close(self):
        del self
        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """get the milliquas object

        **Return:**
            - ``milliquas``

        **Todo**
            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        # self.dictList = self.create_dictionary_of_milliquas()
        # self.add_data_to_database_table()
        self.add_htmids_to_database_table()

        self.log.info('completed the ``get`` method')
        return milliquas

    def create_dictionary_of_milliquas(
            self):
        """create dictionary of milliquas

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean create_dictionary_of_milliquas method
            - @review: when complete add logging
        """
        self.log.info('starting the ``create_dictionary_of_milliquas`` method')

        dictList = []
        lines = string.split(self.mqData, '\n')
        inserts = [
            11, 25, 51, 57, 64, 71, 75, 78, 81, 89, 97, 106, 110, 134, 158, 181]
        keys = ["raDeg", "decDeg", "name", "descrip", "rmag", "bmag", "comment", "r_psf_class", "b_psf_class", "z",
                "src_cat_name", "src_cat_z", "qso_prob", "x_name", "r_name", "alt_id1", "alt_id2"]

        totalCount = len(lines)
        count = 0

        for line in lines:
            count += 1
            if count > 1:
                # Cursor up one line and clear line
                sys.stdout.write("\x1b[1A\x1b[2K")
            print "%(count)s / %(totalCount)s milliquas data added to memory" % locals()

            thisDict = {}
            for insert in inserts:
                line.replace("–", "-")
                line = line[:insert] + "|" + line[insert:]

            theseValues = string.split(line, '|')
            for k, v in zip(keys, theseValues):
                v = v.strip()
                if len(v) == 0 or v == "-":
                    v = None
                thisDict[k] = v
            dictList.append(thisDict)

        self.log.info(
            'completed the ``create_dictionary_of_milliquas`` method')
        return dictList

    # use the tab-trigger below for new method
    def add_data_to_database_table(
            self):
        """add data to database table

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean add_data_to_database_table method
            - @review: when complete add logging
        """
        self.log.info('starting the ``add_data_to_database_table`` method')

        dms.insert_list_of_dictionaries_into_database(
            dbConn=self.cataloguesDbConn,
            log=self.log,
            dictList=self.dictList,
            dbTableName=dbTableName,
            uniqueKeyList=["raDeg", "name"],
        )

        self.log.info('completed the ``add_data_to_database_table`` method')
        return None

    # use the tab-trigger below for new method
    def add_htmids_to_database_table(
            self):
        """add htmids to database table

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean add_htmids_to_database_table method
            - @review: when complete add logging
        """
        self.log.info('starting the ``add_htmids_to_database_table`` method')

        from dryxPython import mysql as dms
        dms.add_HTMIds_to_mysql_tables.add_HTMIds_to_mysql_tables(
            raColName="raDeg",
            declColName="decDeg",
            tableName=self.dbTableName,
            dbConn=self.cataloguesDbConn,
            log=self.log,
            primaryIdColumnName="primaryId"
        )

        self.log.info('completed the ``add_htmids_to_database_table`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx

# xt-class-tmpx


###################################################################
# PUBLIC FUNCTIONS                                                #
###################################################################
# xt-worker-def

# use the tab-trigger below for new function
# xt-def-with-logger

###################################################################
# PRIVATE (HELPER) FUNCTIONS                                      #
###################################################################

if __name__ == '__main__':
    main()
