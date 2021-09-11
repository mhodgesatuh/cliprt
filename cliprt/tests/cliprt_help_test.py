#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from IPython.utils.capture import capture_output
from cliprt.classes.cliprt_help import CliprtHelp

class CliprtHelpTest:

    def init_test(self):
        """
        """
        with capture_output() as captured:
            CliprtHelp('./cliprt/resources');
        captured()
        assert len(captured.stdout) > 100