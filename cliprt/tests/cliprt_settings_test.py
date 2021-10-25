#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.cliprt_settings import CliprtSettings

class CliprtSettingsTest:
    """
    Data element dictionary settings test harness.
    """
    settings = CliprtSettings()

    def format_data_elements_test(self):
        """
        Unit test
        """
        assert self.settings.format_date('1-1-21') == \
            '01/01/2021'
        assert self.settings.format_name('Doe, John') == \
            'John Doe'
        assert self.settings.format_phone('3214321', '999', '1') == \
            '1-999-321-4321'
        assert self.settings.format_phone('8883214321', '999', '1') == \
            '1-888-321-4321'
        assert self.settings.format_phone('17773214321') == \
            '1-777-321-4321'
        assert self.settings.format_phone('321-321') == \
            '321-321'

    def format_name_test(self):
        """
        Unit test
        """
        assert self.settings.format_name('name') == 'name'

    def str_normalize_test(self):
        """
        Unit test
        """
        assert self.settings.str_normalize('Abc_deF') == 'abc def'
