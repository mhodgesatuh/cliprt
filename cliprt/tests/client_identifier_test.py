#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry
from cliprt.classes.client_identifier import ClientIdentifier

class ClientIdentifierTest:

    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )
    # Identifier types in the DED to create a client.
    ded_processor.hydrate_ded()
    client_id = ClientIdentifier('phone', '1-800-123-1234', ded_processor.ded)

    def init_test(self):
        """
        """
        assert str(self.client_id) == 'phone::18001231234'

    def save_client_idno_test(self):

        self.client_id.save_client_idno('9989')
        assert '9989' in self.client_id.client_ids