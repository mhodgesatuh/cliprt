#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry
from cliprt.classes.client_identity import ClientIdentity

from cliprt.classes.destination_worksheet import DestinationWorksheet

class DestinationWorksheetsRegistryTest: 
    """
    Client identity test harness.
    """
    # Dependencies
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()
    client_info.create_ded_worksheet(save_wb = False)

    # Test data
    #client_info.create_client_reports(progress_reporting_is_disabled = True, save_wb = False)

    def init_test(self):
        """
        Unit test
        """
        self.client_info.create_client_reports(progress_reporting_is_disabled = True, save_wb = False)

        assert False