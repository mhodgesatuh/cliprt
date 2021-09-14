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

class ClientIdentifierRegistryTest:
    """
    Client identifier registry test harness.
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
    client_id_registry = ClientIdentityRegistry(dest_ws_registry)

    # Test data
    identifier_registry = ClientIdentifierRegistry(client_id_registry)
    identifier = ClientIdentifier('email', 'tester@tst.biz', ded_processor.ded)

    def add_identifier_test(self):
        """
        Unit test
        """
        self.identifier_registry.add_identifier(self.identifier)
        assert len(self.identifier_registry.identifier_list) == 1
