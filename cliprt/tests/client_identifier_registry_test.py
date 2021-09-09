#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identifier import ClientIdentifier
from cliprt.classes.client_identity_registry import ClientIdentityRegistry
from cliprt.classes.client_identifier_registry import ClientIdentifierRegistry
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_processor import DataElementDictionaryProcessor
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry

class ClientIdentifierRegistryText:

    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    dest_ws_registry = DestinationWorksheetsRegistry()
    ded_processor = DataElementDictionaryProcessor(
        client_info.wb, 
        client_info.ded_ws, 
        dest_ws_registry
    )
    client_info.create_client_reports(False)

    identifier_registry = ClientIdentifierRegistry(client_id_registry)

    def add_identifier_test(self):
        """
        """
        client_id = ClientIdentifier()
        assert False
