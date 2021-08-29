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
    HELP_TEXT_PATH = './resources/cliprt_help.txt'

    def __init__(self):
        """
        Print the help text to the console.
        """
        help_text_file = open(self.HELP_TEXT_PATH)
        print(help_text_file.read())
        help_text_file.close()