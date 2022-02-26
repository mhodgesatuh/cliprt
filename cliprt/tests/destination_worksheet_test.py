#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.cliprt_settings import CliprtSettings
from cliprt.classes.destination_worksheet import DestinationWorksheet

class DestinationWorksheetTest:
    """
    Data destination worksheet testing harness.
    """
    # Test data.
    cliprt_wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(cliprt_wb_file)
    dest_ws = DestinationWorksheet(client_info.cliprt_wb, 'fb')
    client_info.dest_ws_reg.add_ws(client_info.cliprt_wb, 'fb')
    settings = CliprtSettings()

    def init_test(self):
        """
        Unit test
        """
        assert self.dest_ws.dest_ind == 'fb'
        assert self.dest_ws.first_row_idx == 1
        assert self.dest_ws.next_col_idx == 1
        assert self.dest_ws.next_row_idx == 2
        assert self.dest_ws.cliprt_ws_name == self.dest_ws.dest_ws_name_prefix + 'fb'
        assert not self.dest_ws.cliprt_ws is None

    def update_cell_test(self):
        """
        Unit test
        """
        # Empty cell data test.
        assert self.dest_ws.update_cell(2, 1, None)

        # Formatted data tests.
        assert self.dest_ws.update_cell(3, 1, '12/31/2021', self.settings.date_format)
        assert self.dest_ws.update_cell(3, 2, 'Doe, John', self.settings.name_format)
        assert self.dest_ws.update_cell(3, 3, '123-1234', self.settings.phone_format)

        # Identical data avoidance test.
        self.dest_ws.update_cell(4, 1, 'cell_data')
        self.dest_ws.update_cell(4, 1, 'cell_data')
        assert self.dest_ws.cliprt_ws.cell(4, 1).value == 'cell_data'

        # Data collection test.
        self.dest_ws.update_cell(4, 1, 'cell_data_02')
        assert self.dest_ws.cliprt_ws.cell(4, 1).value == 'cell_data, cell_data_02'

    def update_column_headings_test(self):
        """
        Unit test
        """
        self.dest_ws.dest_de_list['de_heading'] = 1
        self.dest_ws.update_column_headings()
        assert self.dest_ws.cliprt_ws.cell(1, 1).value == 'de_heading'
