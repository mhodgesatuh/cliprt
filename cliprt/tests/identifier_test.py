#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.identifier import Identifier

class IdentifierTest:
    """
    Data element unit testing harness.
    """
    client_wb_file = 'cliprt/tests/resources/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(client_wb_file)
    client_info.ded_processor.hydrate_ded()

    # Test data
    client_id = Identifier('phone', '1 (800) 123-1234', client_info.ded_processor.ded)
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

    def make_searchable_test(self):
        """
        Unit test.
        """
        assert self.client_id.make_searchable(' aBcD ') == 'abcd'

    def save_client_idno_test(self):
        """
        Unit test
        """
        assert '9989' in self.client_id.client_ids
