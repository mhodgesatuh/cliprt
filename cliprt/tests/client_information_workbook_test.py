#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
import pytest
from mock import patch, Mock
import openpyxl
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.message_registry import MessageRegistry

class ClientInformationWorkbookTest:
    """
    Client information workbook test harness.
    """
    error = MessageRegistry()

    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)

    def init_bad_file_test(self):
        """
        Unit test
        """
        with pytest.raises(Exception) as excinfo:
            client_info_wb = ClientInformationWorkbook('bad_file_name')
        assert 'E1000' in excinfo.value.args[0]

    def create_client_reports_test(self):
        """
        Unit test
        """
        #self.client_info.create_client_reports(False, False)

    def create_content_ws_names_list_test(self):
        """
        Unit test
        """
        # Ignore an existing destination worksheets.
        self.client_info.dest_ws_reg.dest_ws_names.append('dest_ws')
        self.client_info.create_content_ws_names_list()
        assert not 'dest_ws' in self.client_info.content_ws_names