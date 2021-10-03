#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
import pytest
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

    def _create_test_content(self):
        """
        Create a test worksheet from scratch so that we can adjust its
        contents as needed for unit testing.
        """
        test_ws_title = 'test ws'
        if test_ws_title in self.client_info.wb.sheetnames:
            ws = self.client_info.wb[test_ws_title]
            self.client_info.wb.remove(ws)
        self.client_info.wb.create_sheet(test_ws_title)
        return ContentWorksheet(
            self.client_info.ded_processor.wb, 
            test_ws_title,
            self.client_info.ded_processor, 
            self.client_info.client_reg, 
            self.client_info.identifier_reg,
            self.client_info.dest_ws_reg
        )

    def _update_test_content_ws(self, ws, test_data):
        """
        Update the test worksheet with test data for unit testing.
        """
        row_idx = 0
        for test_row in test_data:
            row_idx += 1
            col_idx = 0
            for test_value in test_row:
                col_idx += 1
                ws.cell(row=row_idx, column=col_idx, value=test_value)

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

        test_content = self._create_test_content();
        test_data = [
            ['not in ded', 'client id', 'phone', 'first name', 'last name'],
            ['rubbish', '100', '999-123-1234', 'jane', 'doe']
        ]
        self._update_test_content_ws(test_content.ws, test_data)
        test_content.build_etl_map()
        assert not 'not in ded' in test_content.de_names

    def client_report_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content();
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name'],
            ['100000', '101', '999-123-1201', 'jane1', 'doe'],
            ['100001', '102', '999-123-1202', 'jane1', 'doe'],

        ]
        self._update_test_content_ws(test_content.ws, test_data)
        with capture_output() as captured:
            test_content.client_report()
        captured()
        assert len(captured.stdout) > 100

        test_content = self._create_test_content();
        with capture_output() as captured:
            retval = test_content.client_report()
        captured()
        assert '(W5000)' in captured.stdout
        assert not retval

    def process_row_de_identifiers_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content();
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name'],
            ['100000', '101', '999-123-1201', 'jane1', 'doe'],
        ]
        with pytest.raises(Exception) as excinfo:
            test_content.process_row_de_identifiers()
        assert thrown_error_code in excinfo.value.args[0]

    def process_row_de_fragments_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content();
        retval = test_content.process_row_de_fragments(2)
        assert not retval

    def util_str_normalize_test(self):
        """
        Unit test
        """       
        assert self.content_ws.util_str_normalize('ABC_efg') == 'abc efg'
