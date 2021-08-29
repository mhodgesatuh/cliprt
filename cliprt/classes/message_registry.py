#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class MessageRegistry:
    """
    The message registry contains all of the message content needed for
    error handling throughout the project.
    
    Since Python programs should have short lines, 73 for comment lines
    and 78 for code, all warning and error messages are consolidated in
    this message registry.  This way we are breaking pythonic rules in
    only one place.
    """

    def __init__(self):
        """
        Initialize the list of available messages.
        """
        # Class attributes.
        self.msg = {}

        self.assign_message_content()

    def assign_message_content(self):
        """
        Assign message content.
        """
        # cliprt
        self.msg[1000] = 'Error: required workbook {} not found.'
        self.msg[1001] = 'Warning: Data Element worksheet not found...please wait while it is being created.'
        self.msg[1002] = 'Error: first create and configure the DED worksheet'
        self.msg[1003] = 'Error: First use an Excel compatible editor to configure the DED workshet.'
        self.msg[1004] = 'Error: you first need to intialize and configure the DED worksheet.'
        self.msg[1005] = 'Error: the DED is not available or not ready.'
        # data element dictionary
        self.msg[3000] = 'WS Error: required column heading {} not found in worksheet {}.\nUnable to continue.'
        self.msg[3001] = 'DED Error: specify either a "Dest WS" or a "Dest Element" for {}, but not both.\nUnable to continue.  See example worksheet {} for comparison.'
        self.msg[3002] = 'DED Error: see column "Dest Element" for invalid entry "{}".  It must reference a entry in the colum "Data Element".\nUnable to continue until you correct the worksheet.'
        self.msg[3003] = 'DED Error: Destination format error for {} in worksheet {}. Fragment="n" where "n" is an integer is required.\nUnable to continue.'
        self.msg[3004] = 'DED Error: invalid destination format "{}" specified for "{}". A fragment can only reference an identifier.\nUnable to continue until you remove "identifier".'
        self.msg[3005] = 'DED Error: invalid destination format "{}" specified for "{}".\nUnable to continue.  Valid values: {}.'
        self.msg[3006] = 'DED Error: invalid destination format "{}" specified for "{}".  fragment="n" expected.\nUnable to continue.  Valid values: {}.'
        self.msg[3007] = 'DED Error: the Data Element worksheet has not been configured.  There are as yet no reporting requirements provided.'
        # client information workbook
        self.msg[4000] = 'Error: the Data Element worksheet, "{}", must designate the destination report indicators.  Configuration is incomplete.'
        # content ws
        self.msg[5000] = 'DED Error, data element "{}" specifies an invalid destination: "{}".\nUnable to continue until you correct the DED.'
        self.msg[5001] = 'DED Error, data element "{}" data type not determined: "{}".\nUnable to continue until you correct the DED.'
        self.msg[5002] = 'DED Error, cannot map "{}" to destination data element "{}" since the latter is a fragment.\nUnable to continue until you correct the DED.'
        self.msg[5003] = 'Client Worksheet Error: none of the columns in "{}" match any identifier data elements.  Check your DED.\nUnable to continue until you correct the worksheet or the DED.'

    def msg(self, idx):
        """
        Return message content.
        """
        return self.msg[idx]