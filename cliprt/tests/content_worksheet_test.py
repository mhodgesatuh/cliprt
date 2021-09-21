#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from IPython.utils.capture import capture_output
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.content_worksheet import ContentWorksheet

class ContentWorksheetTest:
    """
    Content worksheet test harness.    
    """
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()

    # Test data
    content_ws_name = client_info.wb.sheetnames[2]
    content_ws = ContentWorksheet(
        client_info.ded_processor.wb, 
        content_ws_name,
        client_info.ded_processor, 
        client_info.client_reg, 
        client_info.identifier_reg,
        client_info.dest_ws_reg
    )

    def build_etl_map_test(self):
        """
        Unit test
        """
        self.content_ws.build_etl_map()
        assert len(self.content_ws.frag_assembler_list) == 1
        assert len(self.content_ws.identifier_col_names) == 4
        assert len(self.content_ws.dest_ws_reg.dest_ws_by_ind_list) == 2
        assert len(self.content_ws.dest_ws_reg.dest_ws_list) == 2
        assert len(self.content_ws.dest_ws_reg.dest_ws_names) == 2

    def client_report_test(self):
        """
        Unit test
        """
        with capture_output() as captured:
            self.content_ws.client_report()
            #self.client_info.create_client_reports(save_wb=False)
        captured()
        assert len(captured.stdout) > 100

    def util_str_normalize_test(self):
        """
        Unit test
        """       
        assert self.content_ws.util_str_normalize('ABC_efg') == 'abc efg'
