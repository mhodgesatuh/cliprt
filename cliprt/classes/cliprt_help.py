#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class CliprtHelp:
    """
    Interactive help text available from the command line. 
    """
    HELP_TEXT_FILE = '/cliprt_help.txt'

    def __init__(self, help_text_path = './cliprt/resources'):
        """
        Print the help text to the console.  The default assumes that
        the call is from the cliprt CLI script.  Unit testing requires 
        another path.
        """
        help_text_file = open(help_text_path + self.HELP_TEXT_FILE)
        print(help_text_file.read())
        help_text_file.close()