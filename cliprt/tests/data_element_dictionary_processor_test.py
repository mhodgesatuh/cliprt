#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
import pytest
from IPython.utils.capture import capture_output
from cliprt.classes.client_information_workbook import ClientInformationWorkbook
from cliprt.classes.data_element_dictionary_settings import DataElementDictionarySettings
from cliprt.classes.message_registry import MessageRegistry

class DataElementDictionaryProcessorTest:
    """
    Data element dictionary processor test harness.
    """
    # Dependencies
    error = MessageRegistry()
    settings = DataElementDictionarySettings()

    # Client workbook with a configured.
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)

    # Client workbook with no DED.
    noded_wb_file = 'cliprt/tests/test_noded_workbook.xlsx'
    noded_client_info = ClientInformationWorkbook(noded_wb_file)

    # DED heading column indicies + 1 yields cell columns.
    de_idx = settings.DE_COL_IDX + 1
    dest_ws_idx = settings.DEST_WS_COL_IDX + 1
    dest_de_idx = settings.DEST_DE_COL_IDX + 1
    format_idx = settings.DE_FORMAT_COL_IDX + 1

    """
    Helper functions for the unit tests start with an '_'.
    """

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
        if not ded_processor.ws.cell(row=4, column=self.de_idx).value == "birthday":
            ded_processor.ws.delete_rows(4, 1)

        # To make testing more resilient, also ensure that the original
        # identifiers are restored.
        self._remove_identifiers_temporarily(ded_processor.ws, action="restore")

    def _remove_identifiers_temporarily(self, ws, action="remove"):
        """
        Temporarily replace all identifiers from the worksheet in order 
        to test for a DED that has no defined identifiers.
        """
        if action == 'restore':
            old_str = self.settings.UNIT_TEST_TMP_DESIGNATION
            new_str = 'identifier'
        else:
            old_str = 'identifier'
            new_str = self.settings.UNIT_TEST_TMP_DESIGNATION

        col_idx = self.settings.DE_FORMAT_COL_IDX + 1
        ws_columns = ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=ws.min_row+1)

        de_column = list(ws_columns)[0]
        for cell in de_column:
            if cell.value == None:
                continue
            cell.value = cell.value.replace(old_str, new_str)

    def _test_data_row(self, ws, values=[None, None], test_row=4):
        """
        Insert or remove test data as needed for custom testing.
        """
        if values[0] == None and values[1] == None:
            ws.delete_rows(test_row, 1)
            return

        ws.insert_rows(test_row, 1)
        ws.cell(row=test_row, column=self.de_idx, value=values[0])
        ws.cell(row=test_row, column=self.dest_ws_idx, value=values[1])
        ws.cell(row=test_row, column=self.dest_de_idx, value=values[2])
        ws.cell(row=test_row, column=self.format_idx, value=values[3])

    def init_test(self):
        """
        Unit test
        """
        # DED worksheet has been created.
        assert self.client_info.has_a_ded_ws()

        # DED worksheet has not been created.
        assert not self.noded_client_info.has_a_ded_ws()

    def bad_ded_config_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor
        test_cases = [
            ['E3150', [None, 'fb', None, None]],
            ['E3170', ['bad dest list', None, 'name,client', None]], 
            ['E3204', ['not two dests', 'fb', 'name', 'name']],
            ['E3207', ['bad dest de', None, 'dest_de', None]],
            ['E3210', ['bad frag', None, 'name', 'fragment=a']],   
            ['E3212', ['bad frag', None, 'client', 'fragment=1']],   
            ['E3214', ['bad frag', None, None, 'name,fragment=1']],
            ['E3215', ['bad frag', None, 'name', 'identifier,fragment=1']],   
            ['E3217', ['bad de format', 'fb', None, 'bad_format']],
            ['E3226', ['bad dest de id', None, 'name', 'identifier']],   
            ['E3232', ['no dest', None, None, None]],
            ['E3238', ['bad dest de', None, 'last name', None]],
        ]
        for thrown_error_code, test_values in test_cases:
            self._dehydrate_ded(test_ded)
            self._test_data_row(test_ded.ws, test_values)
            with pytest.raises(Exception) as excinfo:
                test_ded.hydrate_ded()
            assert thrown_error_code in excinfo.value.args[0]
            self._test_data_row(test_ded.ws)

        # Test for a missing required column heading.
        self._dehydrate_ded(test_ded)
        saved_val = self.client_info.ded_processor.ws.cell(1, 1).value
        self.client_info.ded_processor.ws.cell(1, 1, value='tmp_val')
        with pytest.raises(Exception) as excinfo:
            self.client_info.ded_processor.read_col_headings()
        assert 'E3200' in excinfo.value.args[0]
        self.client_info.ded_processor.ws.cell(1, 1, value=saved_val)

        # Test for an sufficient number of indicaters.
        self._dehydrate_ded(test_ded)
        self._remove_identifiers_temporarily(test_ded.ws)
        with pytest.raises(Exception) as excinfo:
            test_ded.hydrate_ded()
        assert 'E3229' in excinfo.value.args[0]
        self._remove_identifiers_temporarily(test_ded.ws, action='restore')

        # Ensure the DED is reset before running any additional tests.
        self._dehydrate_ded(test_ded)

    def create_ded_worksheet_test(self):
        """
        Unit test
        """
        self.noded_client_info.create_ded_worksheet(save_wb = False)

        # Assert that the new DED worksheet is the very first one.
        assert self.noded_client_info.wb.sheetnames[0] == \
                self.noded_client_info.DED_WS_NAME

        # Assert that the right number of columns headings were created.
        # Create a new DED processor since the workbook has been updaed.
        test_ded = self.noded_client_info.ded_processor
        col_headings = test_ded.read_col_headings()
        assert len(col_headings) == len(test_ded.COL_HEADINGS)

    def hydrate_ded_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Hydrate when already hydrated test.
        test_ded.hydrate_ded()
        test_ded.hydrate_ded()
        assert test_ded.ded_is_hydrated()

    def print_report_test(self):
        """
        Unit test
        """
        self._dehydrate_ded(self.client_info.ded_processor)
        with capture_output() as captured:
            self.client_info.ded_processor.print_report()
        captured()
        assert len(captured.stdout) > 100

    def util_str_normalize_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor
        assert 'abc def' == test_ded.util_str_normalize('Abc_deF')
    
    def util_make_list_test(self):
        """
        Unit test
        """
        str = 'welcome,to ,cliprt'
        str_list = self.client_info.ded_processor.util_make_list(str)
        assert len(str_list) == 3

    def process_dest_de_format_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Bad format test.
        with pytest.raises(Exception) as excinfo:
            test_ded.process_dest_de_format('bad_de', 'bad_format')
        assert 'E3217' in excinfo.value.args[0]

        # Bad fragment test.
        with pytest.raises(Exception) as excinfo:
            test_ded.process_dest_de_format('bad_de', 'fragment')
        assert 'E3220' in excinfo.value.args[0]

    def parse_dest_de_format_str_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Bad fragment index test.
        with pytest.raises(Exception) as excinfo:
            test_ded.parse_dest_de_format_str('bad frag_idx', 'name,fragment=')
        assert 'E3210' in excinfo.value.args[0]

        # Fragments required a destination data element for assembly.
        # todo