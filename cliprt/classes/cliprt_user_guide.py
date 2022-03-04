#!/usr/bin/env python
#pylint: disable=too-few-public-methods
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
from cliprt.classes.cliprt_settings import CliprtSettings

class CliprtUserGuide:
    """
    User guide available from the command line.
    """
    settings = CliprtSettings()
    user_guide_resource = '/cliprt_user_guide.txt'

    def __init__(self, user_guide_path=None):
        """
        Print the user guide to the console.  The default assumes that
        the call is from the cliprt CLI script.  Unit testing requires
        another path.
        """
        if user_guide_path is None:
            user_guide_path = '.' + self.settings.resources_path
        user_guide_file = user_guide_path + self.user_guide_resource
        with open(user_guide_file, "r", encoding='utf8') as user_guide_text:
            print(user_guide_text.read())
