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
    """
    Data element unit testing harness.
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
    client_id = ClientIdentifier('phone', '1-800-123-1234', ded_processor.ded)
    client_id.save_client_idno('9989')

    def init_test(self):
        """
        Unit test
        """
        assert str(self.client_id) == 'phone::18001231234'

    def repr_test(self):
        """
        Unit test
        """
        assert self.client_id.__repr__() == 'phone::18001231234'

    def save_client_idno_test(self):
        """
        Unit test
        """
        assert '9989' in self.client_id.client_ids

    def add_identifier_to_registry_test(self):
        """
        Unit test
        """
        identifier = ClientIdentifier('phone', '1-999-123-9999', self.ded_processor.ded)
        id_registry = self.client_info.identifier_registry
        if not identifier.key in id_registry.identifier_list.items():
            id_registry.identifier_list[identifier.key] = identifier
        assert False