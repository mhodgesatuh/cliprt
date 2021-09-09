#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
import pytest
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry
from cliprt.classes.message_registry import MessageRegistry

class DataElementDictionaryProcessorTest:

    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )

    preconfig_wb_file = 'cliprt/tests/test_preconfig_workbook.xlsx'
    preconfig_client_info = ClientInformationWorkbook(preconfig_wb_file)
    preconfig_dest_ws_registry = DestinationWorksheetsRegistry()
    preconfig_ded_processor = DataElementDictionaryProcessor(
        preconfig_client_info.wb, 
        preconfig_client_info.ded_ws, 
        preconfig_dest_ws_registry
    )
    
    noded_wb_file = 'cliprt/tests/test_noded_workbook.xlsx'
    noded_client_info = ClientInformationWorkbook(noded_wb_file)
    noded_dest_ws_registry = DestinationWorksheetsRegistry()
    noded_ded_processor = DataElementDictionaryProcessor(
        noded_client_info.wb, 
        noded_client_info.ded_ws, 
        noded_dest_ws_registry
    )
    error = MessageRegistry()

    def init_test(self):
        """
        """
        assert self.client_info.has_a_ded_ws() == True
        assert self.ded_processor.ded_is_configured() == True

        assert self.preconfig_client_info.has_a_ded_ws() == True
        assert self.preconfig_ded_processor.ded_is_configured() == False

        assert self.noded_client_info.has_a_ded_ws() == False
        assert self.noded_ded_processor.ded_is_configured() == False

    def create_ded_worksheet_test(self):
        """
        """
        self.noded_client_info.create_ded_worksheet(save_wb = False)

        # Assert that the new DED worksheet is the very first one.
        assert self.noded_client_info.wb.sheetnames[0] == self.noded_client_info.DED_WS_NAME

        # Assert that the right number of columns headings were created.
        # Create a new DED processor since the workbook has been updaed.
        ded_processor = DataElementDictionaryProcessor(
            self.noded_client_info.wb, 
            self.noded_client_info.ded_ws, 
            self.noded_dest_ws_registry
        )
        col_headings = ded_processor.read_col_headings()
        assert len(col_headings) == len(ded_processor.COL_HEADINGS)

    def format_data_elements_test(self):
        """
        """
        assert self.ded_processor.format_date('1-1-21') == '01/01/2021'
        assert self.ded_processor.format_name('Doe, John') == 'John Doe'
        assert self.ded_processor.format_phone('3214321', '999', '1') == '1-999-321-4321'
        assert self.ded_processor.format_phone('8883214321', '999', '1') == '1-888-321-4321'
        assert self.ded_processor.format_phone('18883214321') == '1-888-321-4321'
        assert self.ded_processor.format_phone('321-321') == '321-321'

    def hydrate_ded_test(self):
        """
        """
        self.ded_processor.hydrate_ded()
        assert self.ded_processor.ded_is_hydrated() == True

    def hydrate_preconfig_ded_test(self):
        """
        """
        with pytest.raises(Exception) as excinfo:
            self.preconfig_ded_processor.hydrate_ded()
            assert False

    def util_str_normalize_test(self):
        """
        """
        assert 'abc def' == self.ded_processor.util_str_normalize('Abc_deF')
    
    def util_make_list_test(self):
        """
        """
        str = 'welcome,to ,cliprt'
        str_list = self.ded_processor.util_make_list(str)
        assert len(str_list) == 3

    def validate_dest_de_list_test(self):
        """
        """
        col_headings = self.ded_processor.read_col_headings()
        assert len(col_headings) >= len(self.ded_processor.COL_HEADINGS)
        assert self.ded_processor.validate_dest_de_list(col_headings) == True