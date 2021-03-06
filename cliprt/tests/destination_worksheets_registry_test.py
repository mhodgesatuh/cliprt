#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.destination_worksheet import DestinationWorksheet

class DestinationWorksheetsRegistryTest:
    """
    Client destination worksheet registry test harness.
    """
    # Test data
    client_wb_file = 'cliprt/tests/resources/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(client_wb_file)
    dest_ws = DestinationWorksheet(client_info.cliprt_wb, 'fb')
    client_info.dest_ws_reg.add_ws(client_info.cliprt_wb, 'fb')

    def add_de_name_test(self):
        """
        Unit test
        """
        self.client_info.dest_ws_reg.add_de_name('fb', 'de_name', 1)
        assert len(self.client_info.dest_ws_reg.dest_ws_by_ind_list) == 1
        assert len(self.client_info.dest_ws_reg.dest_ws_list) == 1
        assert len(self.client_info.dest_ws_reg.dest_ws_names) == 1

    def add_ws_test(self):
        """
        Unit test
        """
        # Duplicate add test.
        self.client_info.dest_ws_reg.add_ws(self.client_info.cliprt_wb, 'fb')
        assert len(self.client_info.dest_ws_reg.dest_ws_by_ind_list) == 1

    def get_next_col_idx_test(self):
        """
        Unit test
        """
        assert self.client_info.dest_ws_reg.get_next_col_idx('fb') == 1

    def prep_worksheets_test(self):
        """
        Unit test
        """
        dest_ws = self.client_info.dest_ws_reg.dest_ws_by_ind_list['fb']
        dest_ws.dest_de_list['de_heading'] = 1
        self.client_info.dest_ws_reg.prep_worksheets()
        assert self.dest_ws.cliprt_ws.cell(1, 1).value == 'de_heading'

    def update_dest_ws_cell_test(self):
        """
        Unit test
        """
        self.client_info.dest_ws_reg.update_dest_ws_cell('fb', 2, 1, 'cell_data')
        assert self.dest_ws.cliprt_ws.cell(2, 1).value == 'cell_data'
