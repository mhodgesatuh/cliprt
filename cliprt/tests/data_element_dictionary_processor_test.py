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
    """
    Data element dictionary processor test harness.
    """
    # Dependencies
    error = MessageRegistry()

    # Dependencies
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    # Test data
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )

    # Dependencies
    preconfig_wb_file = 'cliprt/tests/test_preconfig_workbook.xlsx'
    preconfig_client_info = ClientInformationWorkbook(preconfig_wb_file)
    preconfig_dest_ws_registry = DestinationWorksheetsRegistry()
    # Test data
    preconfig_ded_processor = DataElementDictionaryProcessor(
        preconfig_client_info.wb, 
        preconfig_client_info.ded_ws, 
        preconfig_dest_ws_registry
    )
    
    # Dependencies
    noded_wb_file = 'cliprt/tests/test_noded_workbook.xlsx'
    noded_client_info = ClientInformationWorkbook(noded_wb_file)
    noded_dest_ws_registry = DestinationWorksheetsRegistry()
    # Test data
    noded_ded_processor = DataElementDictionaryProcessor(
        noded_client_info.wb, 
        noded_client_info.ded_ws, 
        noded_dest_ws_registry
    )

    def init_test(self):
        """
        Unit test
        """
        # DED worksheet has been created and configured.
        assert self.client_info.has_a_ded_ws()
        assert self.ded_processor.ded_is_configured()

        # DED worksheet has been created but is not yet manually 
        # configured.
        assert self.preconfig_client_info.has_a_ded_ws()
        assert not self.preconfig_ded_processor.ded_is_configured()

        # DED worksheet has not been created.
        assert not self.noded_client_info.has_a_ded_ws()
        assert not self.noded_ded_processor.ded_is_configured()

    def create_ded_worksheet_test(self):
        """
        Unit test
        """
        self.noded_client_info.create_ded_worksheet(save_wb = False)

        # Assert that the new DED worksheet is the very first one.
        assert self.noded_client_info.wb.sheetnames[0] == \
                self.noded_client_info.DED_WS_NAME

        # Assert that the right number of columns headings were created.
        # Create a new DED processor since the workbook has been updaed.
        ded_processor = DataElementDictionaryProcessor(
            self.noded_client_info.wb, 
            self.noded_client_info.ded_ws, 
            self.noded_dest_ws_registry
        )
        col_headings = ded_processor.read_col_headings()
        assert len(col_headings) == len(ded_processor.COL_HEADINGS)

    def hydrate_ded_test(self):
        """
        Unit test
        """
        self.ded_processor.hydrate_ded()
        assert self.ded_processor.ded_is_hydrated()

    def hydrate_preconfig_ded_test(self):
        """
        Unit test
        """
        with pytest.raises(Exception) as excinfo:
            self.preconfig_ded_processor.hydrate_ded()
            assert False

    def util_str_normalize_test(self):
        """
        Unit test
        """
        assert 'abc def' == self.ded_processor.util_str_normalize('Abc_deF')
    
    def util_make_list_test(self):
        """
        Unit test
        """
        str = 'welcome,to ,cliprt'
        str_list = self.ded_processor.util_make_list(str)
        assert len(str_list) == 3

    def validate_dest_de_list_test(self):
        """
        Unit test
        """
        col_headings = self.ded_processor.read_col_headings()
        assert len(col_headings) >= len(self.ded_processor.COL_HEADINGS)
        assert self.ded_processor.validate_dest_de_list(col_headings)