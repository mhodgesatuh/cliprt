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
        self.message = {}

        self.assign_message_content()

    def assign_message_content(self):
        """
        Assign message content.
        """
        utc = '\nUnable to continue until you correct the worksheet. See example the worksheet in /resources.'

        # cliprt
        self.message[1000] = 'Error: required workbook {} not found.'
        self.message[1001] = 'Warning: Data Element worksheet not found...please wait while it is being created.'
        self.message[1002] = 'Error: first create and configure the DED worksheet'
        self.message[1003] = 'Error: First use an Excel compatible editor to configure the DED workshet.'
        self.message[1004] = 'Error: you first need to intialize and configure the DED worksheet.'
        self.message[1005] = 'Error: the DED is not available or not ready.'
        # data element dictionary
        self.message[2500] = 'DED Error: invalid Dest Element" for {}. Dest Element must not be a list: "{}"; only one allowed.' + utc
        self.message[3000] = 'WS Error: required column heading {} not found in worksheet {}.' + utc
        self.message[3001] = 'DED Error: specify either a "Dest WS" or a "Dest Element" for {}, but not both.' + utc
        self.message[3002] = 'DED Error: see column "Dest Element" for invalid entry "{}". It must reference a entry in the colum "Data Element".' + utc
        self.message[3003] = 'DED Error: Destination format error for {} in worksheet {}. Fragment="n" where "n" is an integer is required.' + utc
        self.message[3004] = 'DED Error: invalid destination format "{}" specified for "{}". A fragment must reference a destination data element for assembly.' + utc
        self.message[3005] = 'DED Error: invalid destination format "{}" specified for "{}".\nValid values: {}.' + utc
        self.message[3006] = 'DED Error: invalid destination format "{}" specified for "{}". fragment="n" expected.\nValid values: {}.' + utc
        self.message[3008] = 'DED Error: invalid destination format specified for "{}". A fragment cannot be an identifier.' + utc
        self.message[3009] = 'DED Error: invalid Dest Element "{}" specified for "{}". An identifier cannot be remapped to another Dest Element.' + utc
        self.message[3010] = 'DED Error: no data element name specified for worksheet "{}", cell "{}". Review the row and remove it if not needed.' + utc
        self.message[3011] = 'DED Error: the Data Element worksheet is incomplete. There are as yet no identifiers provided.'
        self.message[3012] = 'DED Error: specify either a "Dest WS" or a "Dest Element" for {}.' + utc
        self.message[3014] = 'DED Error: the Data Element worksheet is incomplete. There are as yet no destination worksheets provided.'
        # client information workbook
        self.message[4000] = 'Error: the Data Element worksheet, "{}", must designate the destination report indicators.  Configuration is incomplete.'
        # content work sheet
        self.message[5000] = 'DED Error, data element "{}" specifies an invalid destination: "{}".' + utc
        self.message[5001] = 'DED Error, data element "{}" data type not determined: "{}".' + utc
        self.message[5002] = 'DED Error, cannot map "{}" to destination data element "{}" since the latter is a fragment.' + utc
        self.message[5003] = 'Client Worksheet Error: none of the columns in "{}" match any identifier data elements.  Check your DED.' + utc

    def msg(self, idx):
        """
        Return message content. 
        Format is: (Ennnn) Error text.
        """
        return '(E{}) {}'.format(idx, self.message[idx])