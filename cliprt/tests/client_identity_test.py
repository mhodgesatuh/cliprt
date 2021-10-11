#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identity import ClientIdentity
from cliprt.classes.client_information_workbook import ClientInformationWorkbook

class ClientIdentityTest:
    """
    Client identity test harness.
    """
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()

    # Test data
    client_id = ClientIdentity('9999', client_info.dest_ws_reg)

    def add_dest_ws_info_test(self):
        """
        Unit test
        """
        self.client_id.add_dest_ws_info(
            self.client_info.dest_ws_reg.dest_ws_by_ind_list
        )
        assert self.client_id.dest_ws == {'ims': 3, 'fb': 3}
        assert self.client_id.get_row_idx('ims') == 3

    def init_test(self):
        """
        Unit test
        """
        assert self.client_id.client_idno == "9999"