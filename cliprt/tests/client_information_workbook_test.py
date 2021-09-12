#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
import openpyxl
import os.path

from cliprt.classes.client_identifier_registry import ClientIdentifierRegistry
from cliprt.classes.client_identity_registry import ClientIdentityRegistry
from cliprt.classes.content_worksheet import ContentWorksheet
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry
from cliprt.classes.message_registry import MessageRegistry

class ClientInformationWorkbook:
    """
    Client information worrkbook test harness.
    """
    # Dependencies

    # Test data

    def __init__(self):
        """
        Ensure that the workbook exists.  Set everything up for 
        processing the workbook.
        """
        if not os.path.exists(wb_filename):
            # Fatal error
            raise Exception(self.error.msg(1000).format(wb_filename))

        # Class attributes.
        self.ded_processor = None
        self.ded_ws = None
        self.dest_ws_registry = DestinationWorksheetsRegistry()
        self.client_id_registry = ClientIdentityRegistry(self.dest_ws_registry)
        self.content_ws_names = []
        self.error = MessageRegistry()
        self.identifier_registry = ClientIdentifierRegistry(self.client_id_registry)
        self.wb = openpyxl.load_workbook(filename=wb_filename)
        self.wb_filename = wb_filename

        # The workbook may or may not have a DED worksheet when it is 
        # iintially accessed.
        self.init_ded_processor()

    def init_test(self):
        """
        Unit test
        """
        False
