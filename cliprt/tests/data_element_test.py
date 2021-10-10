#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.data_element import DataElement
from cliprt.classes.client_information_workbook import ClientInformationWorkbook

class DataElementTest:
    """
    Data element unit testing harness.
    """
    wb_file = 'cliprt/tests/test_workbook.xlsx'
    client_info = ClientInformationWorkbook(wb_file)
    client_info.ded_processor.hydrate_ded()

    # Test data

    data_element = DataElement('test_de', client_info.ded_processor.ded)
    data_element.add_dest_ws_ind('fb', 1)

    remapped_data_element = DataElement('remapped_de', client_info.ded_processor.ded)
    remapped_data_element.add_dest_ws_ind('fb', 2)
    remapped_data_element.set_dest_de_name('dest_de')
    remapped_data_element.set_dest_de_format('phone')

    nodest_data_element = DataElement('nodest_de', client_info.ded_processor.ded)

    frag_data_element = DataElement('frag_de', client_info.ded_processor.ded)
    frag_data_element.set_to_fragment(1)

    identifier_data_element = DataElement('identifier_de', client_info.ded_processor.ded)
    identifier_data_element.set_to_identifier()

    def add_dest_ws_ind_test(self):
        """
        Unit test
        """
        # Test duplication avoidance.
        self.data_element.add_dest_ws_ind('fb', 1)
        assert len(self.data_element.dest_ws_info) == 1

    def get_col_by_dest_ws_ind_test(self):
        """
        Unit test
        """
        assert self.data_element.get_col_by_dest_ws_ind('fb') == 1
        assert not self.data_element.get_col_by_dest_ws_ind('zz')

    def get_identifier_type_test(self):
        """
        Unit test
        """
        assert self.data_element.get_identifier_type() == \
            self.data_element.name
        assert self.remapped_data_element.get_identifier_type() == \
            self.remapped_data_element.dest_de_name

    def has_dest_ws_test(self):
        """
        Unit test
        """
        assert not self.nodest_data_element.has_dest_ws()

    def init_test(self):
        """
        Unit test
        """
        assert self.data_element.is_content
        assert self.data_element.is_mapped_to_dest_ws('fb')
        assert self.data_element.has_dest_ws()
        assert not self.data_element.is_identifier
        assert not self.data_element.is_fragment
        assert not self.data_element.is_remapped

    def set_dest_de_name_test(self):
        """
        Unit test
        """
        assert self.remapped_data_element.dest_de_name == 'dest_de'
        assert self.remapped_data_element.is_remapped
        assert self.remapped_data_element.dest_de_format == 'phone'

    def set_to_fragment_test(self):
        """
        Unit test
        """
        assert self.frag_data_element.fragment_idx == 1
        assert not self.frag_data_element.is_content
        assert self.frag_data_element.is_fragment

    def set_to_identifier_test(self):
        """
        Unit test
        """
        self.data_element.set_to_identifier()
        assert not self.data_element.is_content
        assert self.data_element.is_identifier

    def str_test(self):
        """
        Unit test
        """
        assert self.data_element.__str__() == \
            "is_content, {'fb': {'col_idx': 1}}"
        assert self.remapped_data_element.__str__() == \
            "{'dest_de_name': 'dest_de'}, is_content, {'dest_de_format': 'phone'}, " + \
            "{'fb': {'col_idx': 2}}"
        assert self.frag_data_element.__str__() == \
            "{'fragment_idx': 1}"
        aa = self.identifier_data_element.__str__()
        assert self.identifier_data_element.__str__() == \
            "is_identifier"

    def util_format_dict_output_test(self):
        """
        Unit test
        """
        assert self.data_element.util_format_dict_output('key', 'val') == \
            "{'key': 'val'}"
        assert self.data_element.util_format_dict_output('key', 999) == \
            "{'key': 999}"