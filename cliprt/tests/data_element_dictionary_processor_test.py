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

    # Client workbook with a unconfigure DED.
    preconfig_wb_file = 'cliprt/tests/test_preconfig_workbook.xlsx'
    preconfig_client_info = ClientInformationWorkbook(preconfig_wb_file)
    
    # Client workbook with no DED.
    noded_wb_file = 'cliprt/tests/test_noded_workbook.xlsx'
    noded_client_info = ClientInformationWorkbook(noded_wb_file)

    # DED heading column indicies + 1 yields cell columns.
    de_idx = settings.DE_COL_IDX + 1
    dest_ws_idx = settings.DEST_WS_COL_IDX + 1
    dest_de_idx = settings.DEST_DE_COL_IDX + 1
    format_idx = settings.DE_FORMAT_COL_IDX + 1

    """
    Helper functions for the unit tests.  Start with an '_'.
    """

    def _dehydrate_ded(self, ded_processor):
        """
        Undo the DED hydration in prepartion for a new test.
        """
        ded_processor.de_fragments_list = {}
        ded_processor.ded = {}
        ded_processor.ded_hydrated = False

    def _remove_identifiers_temporarily(self, ws, action="cleanup"):
        """
        Temporarily replace all identifiers from the worksheet in order 
        to test for a DED that has no defined identifiers.
        """
        if action == 'cleanup':
            old_str = 'tmp_id'
            new_str = 'identifier'
        else:
            old_str = 'identifier'
            new_str = 'tmp_id'

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
        # DED worksheet has been created and configured.
        assert self.client_info.has_a_ded_ws()
        assert self.client_info.ded_processor.ded_is_configured()

        # DED worksheet has been created but is not yet manually 
        # configured.
        assert self.preconfig_client_info.has_a_ded_ws()
        assert not self.preconfig_client_info.ded_processor.ded_is_configured()

        # DED worksheet has not been created.
        assert not self.noded_client_info.has_a_ded_ws()
        assert self.noded_client_info.ded_processor == None

    def bad_ded_config_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # todo: incomplete test
        # dest_ws column: no destination worksheet specified
        self._dehydrate_ded(test_ded)
        test_values = ['no dest_ws', None, 'name', 'name']
        self._test_data_row(test_ded.ws, test_values)
        test_ded.hydrate_ded()
        self._test_data_row(test_ded.ws)

        # dest_de column: one or the other, not both dest_de and dest_ws
        self._dehydrate_ded(test_ded)
        test_values = ['bad dest_ws', 'fb', 'name', None]
        self._test_data_row(test_ded.ws, test_values)
        with pytest.raises(Exception) as excinfo:
            test_ded.hydrate_ded()
        assert 'E3001' in excinfo.value.args[0]
        self._test_data_row(test_ded.ws)

        # de_format column: invalid format: date, name, phone only
        self._dehydrate_ded(test_ded)
        test_values = ['bad de_format', 'fb', None, 'email']
        self._test_data_row(test_ded.ws, test_values)
        with pytest.raises(Exception) as excinfo:
            test_ded.hydrate_ded()
        assert 'E3005' in excinfo.value.args[0]
        self._test_data_row(test_ded.ws)

        # data element name column: missing name.
        self._dehydrate_ded(test_ded)
        test_values = [None, 'fb', None, None]
        self._test_data_row(test_ded.ws, test_values)
        with pytest.raises(Exception) as excinfo:
            test_ded.hydrate_ded()
        assert 'E3010' in excinfo.value.args[0]
        self._test_data_row(test_ded.ws)

        # dest_ws column: no dest element should be specified

        # dest_element column: no dest worksheet should be specified

        # dest_element column: dest element must be in the ded

        # dest_element column: dest element must not be a list

        # ded: missing required named column

        # ded: no idicators spexified in the ded.

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

    def ded_is_configured_test(self):
        """
        Unit test
        """
        # Test for detecting in unconfigured DED.
        assert not self.preconfig_client_info.ded_is_configured()

        # Test for no destination worksheet.
        assert not self.preconfig_client_info.ded_is_configured() 
        # Add a destination worksheet for the remaining tests.
        # TODO 

        # Test for a configured DED that has no identifiers.
        self._remove_identifiers_temporarily(
            self.client_info.ded_processor.ws, 
            action='remove'
        )
        assert not self.client_info.ded_is_configured()  
        self._remove_identifiers_temporarily(
            self.client_info.ded_processor.ws, 
            action='cleanup'
        )

        # Test for a configured DED that is missing a required column
        # heading.
        saved_val = self.client_info.ded_processor.ws.cell(1, 1).value
        self.client_info.ded_processor.ws.cell(1, 1, value='tmp_val')
        assert not self.client_info.ded_is_configured()  
        self.client_info.ded_processor.ws.cell(1, 1, value=saved_val)

    def hydrate_ded_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Hydrate when already hydrated test.
        test_ded.hydrate_ded()
        test_ded.hydrate_ded()
        assert test_ded.ded_is_hydrated()

        # Remove the data element from the DED if it does not have a
        # destination worksheet.
        self._dehydrate_ded(test_ded)
        test_values = [
            'no dest_ws',
            None,
            None,
            None
        ]
        self._test_data_row(test_ded.ws, test_values)
        test_ded.hydrate_ded()
        assert not 'no dest_ws' in test_ded.ded
        self._test_data_row(test_ded.ws)

    def hydrate_preconfig_ded_test(self):
        """
        Unit test
        """
        with pytest.raises(Exception) as excinfo:
            self.preconfig_client_info.ded_processor.hydrate_ded()
        assert 'E3007' in excinfo.value.args[0]

    def print_report_test(self):
        """
        Unit test
        """
        with capture_output() as captured:
            self.client_info.ded_processor.print_report()
        captured()
        assert len(captured.stdout) > 100

    def read_col_headings_test(self):
        """
        Unit test
        """
    

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

    def validate_dest_de_list_test(self):
        """
        Unit test
        """
        test_ded = self.preconfig_client_info.ded_processor
        with pytest.raises(Exception) as excinfo:
            col_headings = test_ded.read_col_headings()
            test_ded.validate_dest_de_list(col_headings)
        assert 'E3002' in excinfo.value.args[0]

    def process_dest_de_format_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Bad format test.
        with pytest.raises(Exception) as excinfo:
            test_ded.process_dest_de_format('bad_de', 'bad_format')
        assert 'E3005' in excinfo.value.args[0]

        # Bad fragment test.
        with pytest.raises(Exception) as excinfo:
            test_ded.process_dest_de_format('bad_de', 'fragment')
        assert 'E3006' in excinfo.value.args[0]


    def parse_dest_de_format_str_test(self):
        """
        Unit test
        """
        test_ded = self.client_info.ded_processor

        # Bad fragment index test.
        with pytest.raises(Exception) as excinfo:
            test_ded.parse_dest_de_format_str('bad frag_idx', 'name,fragment=')
        assert 'E3003' in excinfo.value.args[0]

        # Fragments required a destination data element for assembly.
