#!/usr/bin/env python
#pylint: disable=too-few-public-methods
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from IPython.utils.capture import capture_output
from cliprt.classes.cliprt_user_guide import CliprtUserGuide

class CliprtUserGuideTest:
    """
    User guide test harness.
    """
    @staticmethod
    def init_test():
        """
        Unit test
        """
        with capture_output() as captured:
            CliprtUserGuide('./cliprt/resources')
        captured()
        assert len(captured.stdout) > 100
