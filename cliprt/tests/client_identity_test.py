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

class ClientIdentityTest:
    """
    Client identity test harness.
    """
    # Dependencies
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )
    ded_processor.hydrate_ded()

    # Test data
    client_id = ClientIdentity('9999', dest_ws_registry)

    def init_test(self):
        """
        Unit test
        """
        assert self.client_id.client_idno == "9999"

    def add_dest_ws_info_test(self):
        """
        Unit test
        """
        self.client_id.add_dest_ws_info(
            self.dest_ws_registry.dest_ws_by_ind_list
        )
        assert self.client_id.dest_ws == {'ims': 3, 'fb': 3}
        
    def get_row_idx_test(self):
        """
        Unit test
        """
        assert self.client_id.get_row_idx('ims') == 3