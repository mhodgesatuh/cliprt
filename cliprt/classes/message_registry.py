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
        Assign message content.  Message begin with one of the following:
            o 'Error: ...'
            o 'Warning: ...'
        """
        utc =\
            '\nUnable to continue until you correct the worksheet. '\
            'See example the worksheet in /resources.'

        # cliprt
        self.message[1000] =\
            'Error: required workbook {} not found.'
        self.message[1001] =\
            'Warning: Dest WS designation not found...please wait while it is being created.'
        self.message[1002] =\
            'Error: first create and configure the DED worksheet'
        self.message[1003] =\
            'Error: First use an Excel compatible editor to configure the DED workshet.'
        self.message[1004] =\
            'Error: you first need to intialize and configure the DED worksheet.'
        self.message[1005] =\
            'Error: the DED is not available or not ready.'

        # Data element dictionary
        self.message[3150] =\
            'Error: no Content DE Name specified for worksheet "{}", cell "{}". '\
            'Review the row and remove it if not needed.' + utc
        self.message[3170] =\
            'Error: invalid Dest DE Name" for "{}". Dest DE Name must not be a list: "{}"; '\
            'only one allowed.' + utc
        self.message[3200] =\
            'Error: required column heading "{}" not found in worksheet "{}".' + utc
        self.message[3204] =\
            'Error: specify either a "Dest WS" or a "Dest DE Name" for "{}", but not both.' + utc
        self.message[3207] =\
            'Error: see column "Dest DE Name" for invalid entry "{}". '\
            'It must reference a entry in the colum "Data Element".' + utc
        self.message[3210] =\
            'Error: invalid input for "{}". '\
            'Value seen is "{}", {}="n" where "n" is an integer is expected.' + utc
        self.message[3212] =\
            'Error: invalid Dest DE Name "{}" specified for "{}". '\
            'A fragment must reference Dest DE Name with a Dest Ws designation.' + utc
        self.message[3214] =\
            'Error: missing Dest DE Name specified for "{}". '\
            'A fragment must reference a destination data element for assembly.' + utc
        self.message[3215] =\
            'Error: invalid Content DE Type for "{}". Content DE Type must not be a list: '\
            '"{}"; only one allowed.' + utc
        self.message[3217] =\
            'Error: invalid Dest DE Format "{}" specified for "{}".\nValid values: "{}".' + utc
        self.message[3218] =\
            'Error: invalid Content DE Type "{}" specified for "{}".\nValid values: "{}".' + utc
        self.message[3226] =\
            'Error: invalid Dest DE Name "{}" specified for "{}". '\
            'An identifier cannot be remapped to another Dest DE Name.' + utc
        self.message[3229] =\
            'Error: the Dest WS designation is incomplete. There are as yet no identifiers provided.'
        self.message[3232] =\
            'Error: specify either a "Dest WS" or a "Dest DE Name" for "{}".' + utc
        self.message[3238] =\
            'Error: invalid Dest DE Name "{}" specified for "{}". '\
            'A Dest DE Name must have a destination worksheet specified.' + utc

        # Client information workbook
        self.message[4000] =\
            'Error: the Dest WS designation, "{}", must designate the destination report indicators. '\
            'Configuration is incomplete.'

        # Content work sheet
        self.message[5000] =\
            'Warning: insufficient content to report for worksheet {}.'
        self.message[5012] =\
            'Error: none of the columns in "{}" match any identifier data elements. '\
            'Check your DED.' + utc

    def msg(self, msg_no):
        """
        Return message test with its tag.
        """
        return '{} {}'.format(self.msg_tag(msg_no), self.message[msg_no])

    def msg_tag(self, msg_no):
        """
        Create the message tag. Format is:
            (Ennnn) for error messages
            (Wnnnn) for warning messages
        """
        return '({}{})'.format(self.message[msg_no][0], msg_no)