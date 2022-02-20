#!/usr/bin/env python
#pylint: disable=too-few-public-methods
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class CliprtUserGuide:
    """
    User guide available from the command line.
    """

    USER_GUIDE_RESOURCE = '/cliprt_user_guide.txt'

    def __init__(self, user_guide_path='./cliprt/resources'):
        """
        Print the user guide to the console.  The default assumes that
        the call is from the cliprt CLI script.  Unit testing requires
        another path.
        """
        user_guide_file = open(user_guide_path + self.USER_GUIDE_RESOURCE)
        print(user_guide_file.read())
        user_guide_file.close()
