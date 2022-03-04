#!/usr/bin/env python
#pylint: disable=too-few-public-methods
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.identifier import Identifier
from cliprt.classes.cliprt_settings import CliprtSettings

class IdentifierRegistryTest:
    """
    Client identifier registry test harness.
    """
    settings = CliprtSettings()
    client_wb_file = settings.test_resources_path + '/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(client_wb_file)
    client_info.ded_processor.hydrate_ded()
    identifier = Identifier('email', 'tester@tst.biz', client_info.ded_processor.ded)

    def add_identifier_test(self):
        """
        Unit test
        """
        self.client_info.identifier_reg.add_identifier(self.identifier)
        assert len(self.client_info.identifier_reg.identifier_list) == 1
