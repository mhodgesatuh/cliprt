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
from cliprt.classes.cliprt_settings import CliprtSettings
from cliprt.classes.message_registry import MessageRegistry

class DataElementDictionaryProcessorTest:
    """
    Data element dictionary processor test harness.
    """
    error = MessageRegistry()
    settings = CliprtSettings()

    # Client workbook with a configured.
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)

    # Client workbook with no DED.
    noded_wb_file = 'cliprt/tests/test_noded_workbook.xlsx'
    noded_client_info = ClientInformationWorkbook(noded_wb_file)

    # DED heading column indicies + 1 yields cell columns.
    de_idx = settings.de_name_col_idx + 1
    de_type_idx = settings.de_type_col_idx + 1
    dest_ws_idx = settings.dest_ws_col_idx + 1
    dest_de_idx = settings.dest_de_name_col_idx + 1
    dest_format_idx = settings.dest_de_format_col_idx + 1

    # Helper functions for the unit tests start with an '_'.

    def _dehydrate_ded(self, ded_processor):
        """
        Undo the DED hydration in prepartion for a new test.
        """
        ded_processor.de_fragments_list = {}
        ded_processor.ded = {}
        ded_processor.ded_hydrated = False

        # To make testing more resilient, also delete row 4 if it is not
        # set to "birthday" because if it isn't there's still test data
        # left from a previous test.
        if not ded_processor.cliprt_ws.cell(row=4, column=self.de_idx).value == "birthday":
            ded_processor.cliprt_ws.delete_rows(4, 1)

        # To make testing more resilient, also ensure that the original
        # identifiers are restored.
        self._remove_identifiers_temporarily(ded_processor.cliprt_ws, action="restore")

    def _remove_identifiers_temporarily(self, cliprt_ws, action="remove"):
        """
        Temporarily replace all identifiers from the worksheet in order
        to test for a DED that has no defined identifiers.
        """
        if action == 'restore':
            old_str = self.settings.unit_test_de_type
            new_str = 'identifier'
        else:
            old_str = 'identifier'
            new_str = self.settings.unit_test_de_type

        col_idx = self.settings.de_type_col_idx + 1
        ws_columns = cliprt_ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=cliprt_ws.min_row+1)

        de_column = list(ws_columns)[0]
        for cell in de_column:
            if cell.value is None:
                continue
            cell.value = cell.value.replace(old_str, new_str)

    def _test_data_row(self, cliprt_ws, values=None, test_row=4):
        """
        Insert or remove test data as needed for custom testing.
        """
        if values is None:
            cliprt_ws.delete_rows(test_row, 1)
            return

        cliprt_ws.insert_rows(test_row, 1)
        cliprt_ws.cell(row=test_row, column=self.de_idx, value=values[0])
        cliprt_ws.cell(row=test_row, column=self.de_type_idx, value=values[1])
        cliprt_ws.cell(row=test_row, column=self.dest_ws_idx, value=values[2])
        cliprt_ws.cell(row=test_row, column=self.dest_de_idx, value=values[3])
        cliprt_ws.cell(row=test_row, column=self.dest_format_idx, value=values[4])

    def bad_ded_config_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor
        # Test case: de, de type, dest ws, dest de, dest format
        test_cases = [
            ['E3150', [None, None, 'fb', None, None]],
            ['E3170', ['bad dest list', None, None, 'client,id', 'name']],
            ['E3204', ['bad two dests', None, 'fb', 'name', 'name']],
            ['E3207', ['bad dest de', None, None, 'bad_de_name', None]],
            ['E3210', ['bad frag', 'fragment=bad', None, None, None]],
            ['E3212', ['bad frag', 'fragment=1', None, 'client', None]],
            ['E3214', ['bad frag', 'fragment=1', None, None, 'name']],
            ['E3215', ['bad frag', 'fragment=1,identifier', None, 'name', None]],
            ['E3217', ['bad de format', 'fb', None, None, 'bad_format']],
            ['E3226', ['bad dest de id', 'identifier', None, 'name', 'name']],
            ['E3232', ['bad no dest ws', None, None, None, None]],
            ['E3238', ['bad dest de', None, None, 'last name', None]],
            ]
        # Test each test case, one at a time to ensure that it throws
        # the required error.
        for thrown_error_code, test_values in test_cases:
            self._dehydrate_ded(test_ded)
            self._test_data_row(test_ded.cliprt_ws, test_values)
            with pytest.raises(Exception) as excinfo:
                test_ded.hydrate_ded()
            assert thrown_error_code in excinfo.value.args[0]
            self._test_data_row(test_ded.cliprt_ws)

        # Test for a missing required column heading.
        self._dehydrate_ded(test_ded)
        saved_val = self.client_info.ded_processor.cliprt_ws.cell(1, 1).value
        self.client_info.ded_processor.cliprt_ws.cell(1, 1, value='tmp_val')
        with pytest.raises(Exception) as excinfo:
            self.client_info.ded_processor.read_col_headings()
        assert 'E3200' in excinfo.value.args[0]
        self.client_info.ded_processor.cliprt_ws.cell(1, 1, value=saved_val)

        # Test for a missing required column heading.
        self._dehydrate_ded(test_ded)
        saved_val = self.client_info.ded_processor.cliprt_ws.cell(1, 1).value
        self.client_info.ded_processor.cliprt_ws.cell(1, 1, value='tmp_val')
        assert not self.client_info.ded_processor.read_col_headings(evaluate_only=True)
        self.client_info.ded_processor.cliprt_ws.cell(1, 1, value=saved_val)

        # Test for an sufficient number of indicaters.
        self._dehydrate_ded(test_ded)
        self._remove_identifiers_temporarily(test_ded.cliprt_ws)
        with pytest.raises(Exception) as excinfo:
            test_ded.hydrate_ded()
        assert 'E3229' in excinfo.value.args[0]
        self._remove_identifiers_temporarily(test_ded.cliprt_ws, action='restore')

        # Ensure the DED is reset before running any additional tests.
        self._dehydrate_ded(test_ded)

    def create_ded_worksheet_test(self):
        """
        Unit test
        """
        self.noded_client_info.create_ded_worksheet(save_wb=False)

        # Assert that the new DED worksheet is the very first one.
        assert self.noded_client_info.cliprt_wb.sheetnames[0] == \
                self.noded_client_info.DED_WS_NAME

        # Assert that the right number of columns headings were created.
        # Create a new DED processor since the workbook has been updaed.
        test_ded = self.noded_client_info.ded_processor
        col_headings = test_ded.read_col_headings()
        assert len(col_headings) == len(self.settings.col_headings)

    def hydrate_ded_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Hydrate when already hydrated test.
        test_ded.hydrate_ded()
        test_ded.hydrate_ded()
        assert test_ded.ded_is_hydrated()

    def init_test(self):
        """
        Unit test
        """
        # DED worksheet has been created.
        assert self.client_info.has_a_ded_ws()

        # DED worksheet has not been created.
        noded_client_info = ClientInformationWorkbook(self.noded_wb_file)
        assert not noded_client_info.has_a_ded_ws()


    def print_report_test(self):
        """
        Unit test
        """
        self._dehydrate_ded(self.client_info.ded_processor)
        with capture_output() as captured:
            self.client_info.ded_processor.print_report()
        captured()
        assert len(captured.stdout) > 100

    def process_dest_de_format_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Bad format test.
        with pytest.raises(Exception) as excinfo:
            test_ded.process_dest_de_format('bad_de', 'bad_format')
        assert 'E3217' in excinfo.value.args[0]

    def util_make_list_test(self):
        """
        Unit test
        """
        test_str = 'welcome,to ,cliprt'
        test_str_list = self.client_info.ded_processor.util_make_list(test_str)
        assert len(test_str_list) == 3
