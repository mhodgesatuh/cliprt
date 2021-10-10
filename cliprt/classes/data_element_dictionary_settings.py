#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from dateutil.parser import parse

class DataElementDictionarySettings:
    """
    DED settings.  Used in the DED processor as well as the destination
    workbooks.
    todo: separate this into CliprtSettings and CliprtData.  First iteration
        of CliprtSettings will have constants.  Second version maybe an 
        external config file, though with a scripting language that might
        not be worth the trouble.
    """

    # Required DED column headings.
    COL_HEADINGS = ['Data Element', 'Dest WS', 'Dest Element', 'DE Format']
    DE_COL_IDX = 0
    DEST_WS_COL_IDX = 1
    DEST_DE_COL_IDX = 2
    DE_FORMAT_COL_IDX = 3

    # Data element designations overloaded into data element formats.
    FRAGMENT_DESIGNATION = 'fragment'
    IDENTIFIER_DESIGNATION = 'identifier'
    UNIT_TEST_TMP_DESIGNATION = 'unittesttd'

    # Data element formats.
    DATE_FORMAT = 'date'
    NAME_FORMAT = 'name'
    PHONE_FORMAT = 'phone'

    # Valid data element formats.
    VALID_DE_FORMATS = [
        IDENTIFIER_DESIGNATION, 
        FRAGMENT_DESIGNATION, 
        DATE_FORMAT, 
        NAME_FORMAT, 
        PHONE_FORMAT,
        UNIT_TEST_TMP_DESIGNATION,
    ]

    # Minimum number of required identifiers in the DED.
    IDENTIFIERS_MIN = 2

    def format_date(self, date_value):
        """
        Normalize the format of dates if possible.
        """
        date_obj = parse(date_value)
        return date_obj.strftime("%m/%d/%Y")

    def format_name(self, data_value):
        """
        Normalize the format of names if possible.
        """
        name_pieces = data_value.split(",")

        # If there are no pieces there's nothing to do.
        if len(name_pieces) <= 1:
            return data_value

        # Convert format 'last, first' to 'first last'.
        ret_value = ''

        # Start with the 2nd piece.
        # No problem if there are extra commas.
        i = 1
        while i < len(name_pieces):
            ret_value+=name_pieces[i]
            i+=1
        # Last name goes last.
        ret_value+=' '+name_pieces[0]
        return ret_value.strip()

    def format_phone(self, data_value, area_code = '808', country_code = '1'):
        """
        Normalize the format of phone numbers if possible.
        """
        # Digits only.
        pho_no = ''.join(i for i in data_value if i.isdigit())

        # Output mask: 1-999-123-4567
        pho_mask = '{}-{}-{}-{}'

        # Format known phone number data lengths.
        if len(pho_no) == 7:
            return pho_mask.format(
                country_code, 
                area_code, 
                pho_no[0:3], 
                pho_no[3:7]
                )
        elif len(pho_no) == 10:
            return pho_mask.format(
                country_code, 
                pho_no[0:3], 
                pho_no[3:6], 
                pho_no[6:10]
                )
        elif len(pho_no) == 11:
            return pho_mask.format(
                pho_no[0:1], 
                pho_no[1:4], 
                pho_no[4:7], 
                pho_no[7:11]
                )
        else:
            return data_value