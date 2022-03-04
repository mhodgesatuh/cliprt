#!/usr/bin/env python
#pylint: disable=import-error
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
import pytest
from IPython.utils.capture import capture_output
from cliprt.classes.client_identity_resolver import ClientIdentityResolver
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.content_worksheet import ContentWorksheet
from cliprt.classes.cliprt_settings import CliprtSettings

class ContentWorksheetTest:
    """
    Content worksheet test harness.
    """
    settings = CliprtSettings()
    client_wb_file = settings.test_resources_path + '/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(client_wb_file)
    client_info.ded_processor.hydrate_ded()

    # Helper functions for the unit tests start with an '_'.

    def _create_test_content(self, action='create'):
        """
        Create a test worksheet from scratch so that we can adjust its
        contents as needed for unit testing.
        """
        test_ws_title = 'test ws'

        # Remove the worksheet if it got left behind due to a test
        # failure.
        if test_ws_title in self.client_info.cliprt_wb.sheetnames:
            cliprt_ws = self.client_info.cliprt_wb[test_ws_title]
            self.client_info.cliprt_wb.remove(cliprt_ws)

        if action != 'create':
            return False

        self.client_info.cliprt_wb.create_sheet(test_ws_title)
        return ContentWorksheet(
            self.client_info.ded_processor.cliprt_wb,
            test_ws_title,
            self.client_info.ded_processor,
            self.client_info.client_reg,
            self.client_info.identifier_reg,
            self.client_info.dest_ws_reg
            )

    @staticmethod
    def _update_test_content_ws(cliprt_ws, test_data):
        """
        Update the test worksheet with test data for unit testing.
        """
        row_idx = 0
        for test_row in test_data:
            row_idx += 1
            col_idx = 0
            for test_value in test_row:
                col_idx += 1
                cliprt_ws.cell(row=row_idx, column=col_idx, value=test_value)

    def build_etl_map_test(self):
        """
        Unit test
        """
        content_ws_name = self.client_info.cliprt_wb.sheetnames[2]
        content_ws = ContentWorksheet(
            self.client_info.ded_processor.cliprt_wb,
            content_ws_name,
            self.client_info.ded_processor,
            self.client_info.client_reg,
            self.client_info.identifier_reg,
            self.client_info.dest_ws_reg
            )
        content_ws.build_etl_map()
        assert len(content_ws.frag_assembler_list) == 1
        assert len(content_ws.identifier_col_names) == 4
        assert len(content_ws.dest_ws_reg.dest_ws_by_ind_list) == 2
        assert len(content_ws.dest_ws_reg.dest_ws_list) == 2
        assert len(content_ws.dest_ws_reg.dest_ws_names) == 2

        test_content = self._create_test_content()
        # First row: headings; 2nd+ rows: data.
        test_data = [
            ['not in ded', 'client id', 'phone', 'first name', 'last name'],
            ['rubbish', '100', '999-123-1234', 'jane', 'doe']
            ]
        self._update_test_content_ws(test_content.cliprt_ws, test_data)
        test_content.build_etl_map()
        assert 'not in ded' not in test_content.de_names
        self._create_test_content(action='remove')

    def client_report_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content()
        # First row: headings; 2nd+ rows: data.
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name'],
            ['100000', '101', '999-123-1201', 'jane1', 'doe'],
            ['100001', '102', '999-123-1202', 'jane1', 'doe'],
            ]
        self._update_test_content_ws(test_content.cliprt_ws, test_data)
        with capture_output() as captured:
            test_content.client_report()
        captured()
        assert len(captured.stdout) > 100
        self._create_test_content(action='remove')

        test_content = self._create_test_content()
        with capture_output() as captured:
            retval = test_content.client_report()
        captured()
        assert '(W5000)' in captured.stdout
        assert not retval
        self._create_test_content(action='remove')

        test_content = self._create_test_content()
        # First row: headings; 2nd+ rows: data.
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name', 'gender'],
            ['100000', '101', '999-123-1201', 'jane1', 'doe', 'f'],
            ['100022', '122', '999-123-1222', 'jane2', 'doe', None],
            ]
        self._update_test_content_ws(test_content.cliprt_ws, test_data)
        assert test_content.client_report()
        assert test_content.content_cols == {6: 'gender'}
        self._create_test_content(action='remove')

    def process_row_de_fragments_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content()
        assert not test_content.process_row_de_fragments(2)
        self._create_test_content(action='remove')

    def process_row_de_identifiers_test(self):
        """
        Unit test
        """
        test_content = self._create_test_content()
        # First row: headings; 2nd+ rows: data.
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name'],
            ['100000', '101', '999-123-1201', 'jane1', 'doe'],
            ]
        self._update_test_content_ws(test_content.cliprt_ws, test_data)
        identity_resolver = ClientIdentityResolver(
            self.client_info.client_reg,
            self.client_info.identifier_reg
            )
        with pytest.raises(Exception) as excinfo:
            test_content.process_row_de_identifiers(identity_resolver, 2)
        assert '(E5012)' in excinfo.value.args[0]
        self._create_test_content(action='remove')

        test_content = self._create_test_content()
        # First row: headings; 2nd+ rows: data.
        test_data = [
            ['id', 'client id', 'phone', 'first name', 'last name'],
            ['100000', '', None, 'jane1', 'doe'],
            ]
        self._update_test_content_ws(test_content.cliprt_ws, test_data)
        identity_resolver = ClientIdentityResolver(
            self.client_info.client_reg,
            self.client_info.identifier_reg
            )
        test_content.identifier_col_names['id'] = 1
        test_content.process_row_de_identifiers(identity_resolver, 2)
        assert len(identity_resolver.identifiers_matched) == 1
        for identity in identity_resolver.identifiers_matched:
            assert identity.key == 'client id::100000'
        self._create_test_content(action='remove')

    def process_ws_rows_test(self):
        """
        Unit test
        """
        content_ws_name = self.client_info.cliprt_wb.sheetnames[1]
        content_ws = ContentWorksheet(
            self.client_info.ded_processor.cliprt_wb,
            content_ws_name,
            self.client_info.ded_processor,
            self.client_info.client_reg,
            self.client_info.identifier_reg,
            self.client_info.dest_ws_reg
            )
        assert content_ws.cliprt_ws.max_row == 20

        content_ws.build_etl_map()
        assert content_ws.process_ws_rows()
        assert len(self.client_info.cliprt_wb.sheetnames) == 5
        assert 'comm_report_for_ims' in self.client_info.cliprt_wb.sheetnames
        assert 'comm_report_for_fb' in self.client_info.cliprt_wb.sheetnames
        assert self.client_info.dest_ws_reg.dest_ws_list == \
            {'ims': 'comm_report_for_ims', 'fb': 'comm_report_for_fb'}
        assert self.client_info.dest_ws_reg.dest_ws_names == \
            ['comm_report_for_ims', 'comm_report_for_fb']
