#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.data_element_dictionary_settings import DataElementDictionarySettings

class DataElementDictionarySettingsTest:
    """
    Data element dictionary settings test harness.
    """
    ded_processor = DataElementDictionarySettings()

    def format_data_elements_test(self):
        """
        Unit test
        """
        assert self.ded_processor.format_date('1-1-21') == \
            '01/01/2021'
        assert self.ded_processor.format_name('Doe, John') == \
            'John Doe'
        assert self.ded_processor.format_phone('3214321', '999', '1') == \
            '1-999-321-4321'
        assert self.ded_processor.format_phone('8883214321', '999', '1') == \
            '1-888-321-4321'
        assert self.ded_processor.format_phone('17773214321') == \
            '1-777-321-4321'
        assert self.ded_processor.format_phone('321-321') == \
            '321-321'

    def format_name_test(self):
        """
        Unit test
        """
        assert self.ded_processor.format_name('name') == 'name'
