#!/usr/bin/env python
#pylint: disable=import-error
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
import pytest
from IPython.utils.capture import capture_output
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.message_registry import MessageRegistry

class ClientInformationWorkbookTest:
    """
    Client information workbook test harness.
    """
    cliprt = MessageRegistry()

    client_wb_file = 'cliprt/tests/resources/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(client_wb_file)

    def create_client_reports_test(self):
        """
        Unit test
        """
        assert self.client_info.create_client_reports(save_wb=False)
        assert len(self.client_info.client_reg.client_id_list) == 66
        assert self.client_info.client_reg.next_client_idno == 1066
        assert len(self.client_info.identifier_reg.identifier_list) == 246

    def create_content_ws_names_list_test(self):
        """
        Unit test
        """
        self.client_info.dest_ws_reg.dest_ws_names.append('dest_ws')
        self.client_info.create_content_ws_names_list()
        assert 'dest_ws' not in self.client_info.content_ws_names

        test_ws_title = 'test ws'
        test_ws = self.client_info.cliprt_wb.create_sheet(title=test_ws_title)
        self.client_info.dest_ws_reg.dest_ws_names.append(test_ws_title)
        self.client_info.create_content_ws_names_list()
        assert test_ws_title not in self.client_info.content_ws_names
        self.client_info.cliprt_wb.remove(test_ws)

    def create_ded_worksheet_test(self):
        """
        Unit test
        """
        test_ws_title = self.client_info.DED_WS_NAME
        self.client_info.ded_ws = self.client_info.cliprt_wb.create_sheet(
            title=test_ws_title,
            index=0
            )
        assert self.client_info.create_ded_worksheet(False) is False

    def ded_is_verified_test(self):
        """
        Unit test
        """
        assert self.client_info.ded_processor.hydrate_ded()
        assert self.client_info.ded_is_verified()

    @staticmethod
    def init_bad_file_test():
        """
        Unit test
        """
        with pytest.raises(Exception) as excinfo:
            ClientInformationWorkbook('bad_file_name')
        assert 'E1000' in excinfo.value.args[0]

    def print_ded_report_test(self):
        """
        Unit test
        """
        self.client_info.ded_processor.hydrate_ded()
        with capture_output() as captured:
            self.client_info.print_ded_report()
        captured()
        assert len(captured.stdout) > 100
