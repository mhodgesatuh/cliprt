#!/usr/bin/env python
#pylint: disable=too-few-public-methods
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
class CliprtUserGuide:
    """
    User guide available from the command line.
    """
    user_guide_resource = '/cliprt_user_guide.txt'

    def __init__(self, user_guide_path='./cliprt/resources'):
        """
        Print the user guide to the console.  The default assumes that
        the call is from the cliprt CLI script.  Unit testing requires
        another path.
        """
        user_guide_file = user_guide_path + self.user_guide_resource
        with open(user_guide_file, "r", encoding='utf8'):
            print(user_guide_file.read())
