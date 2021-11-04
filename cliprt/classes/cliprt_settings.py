#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from dateutil.parser import parse

class CliprtSettings:
    """
    Constants, settings, and data formatting functions.
    - DED settings standardize the data element dictionary.
    - Reporting parameters control the output to the destination
        worksheets.
    """

    # ---------------------------------
    # Client content reporting settings
    # ---------------------------------

    # Threshold for determining that we have an identity match.
    IDENTITY_MATCH_THRESHOLD = 2

    # Minimal number of data elements in a client content worksheet
    # required for creating a destination (reporting) worksheet.
    MIN_REQUIRED_CONTENT_WS_COLUMNS = 3

    # Default country code for the phone number format.
    DEFAULT_COUNTRY_CODE = '1'

    # Default area code for the phone number format.
    DEFAULT_AREA_CODE = '808'

    """
    DED Settings
    """
    # Required DED column headings.
    COL_HEADINGS = [
        'Content DE Name',
        'Content DE Type',
        'Dest WS',
        'Dest DE Name',
        'Dest DE Format',
    ]
    DE_NAME_COL_IDX = 0
    DE_TYPE_COL_IDX = 1
    DEST_WS_COL_IDX = 2
    DEST_DE_NAME_COL_IDX = 3
    DEST_DE_FORMAT_COL_IDX = 4

    # Valid data element types.
    FRAGMENT_DE_TYPE = 'fragment'
    IDENTIFIER_DE_TYPE = 'identifier'
    UNIT_TEST_DE_TYPE = 'unittestdet'

    # Valid data element formats.
    DATE_FORMAT = 'date'
    NAME_FORMAT = 'name'
    PHONE_FORMAT = 'phone'

    # Valid data element types list.
    VALID_DE_TYPES = [
        IDENTIFIER_DE_TYPE,
        FRAGMENT_DE_TYPE,
        UNIT_TEST_DE_TYPE,
    ]

    # Valid data element formats list.
    VALID_DE_FORMATS = [
        DATE_FORMAT,
        NAME_FORMAT,
        PHONE_FORMAT,
    ]

    """
    Data formatting functions.
    """
    @staticmethod
    def format_date(date_value):
        """
        Normalize the format of dates if possible.
        """
        date_obj = parse(date_value)
        return date_obj.strftime("%m/%d/%Y")

    @staticmethod
    def format_name(data_value):
        """
        Normalize the format of names if possible to First Last.
        """
        name_pieces = data_value.split(",")

        # If there are no pieces there's nothing to do.
        if len(name_pieces) <= 1:
            return data_value

        # Convert format 'last, first' to 'first last'. Start with the
        # 2nd piece. No problem if there are extra commas.
        ret_value = ''
        i = 1
        while i < len(name_pieces):
            ret_value += name_pieces[i]
            i += 1
        # Last name goes last.
        ret_value += ' ' + name_pieces[0]
        return ret_value.strip()

    def format_phone(self, data_value, area_code=None, country_code=None):
        """
        Normalize the format of phone numbers if possible.
        """
        if country_code is None:
            country_code = self.DEFAULT_COUNTRY_CODE

        if area_code is None:
            area_code = self.DEFAULT_AREA_CODE

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
        if len(pho_no) == 10:
            return pho_mask.format(
                country_code,
                pho_no[0:3],
                pho_no[3:6],
                pho_no[6:10]
            )
        if len(pho_no) == 11:
            return pho_mask.format(
                pho_no[0:1],
                pho_no[1:4],
                pho_no[4:7],
                pho_no[7:11]
            )
        return data_value

    @staticmethod
    def str_normalize(str_value):
        """
        Lowercase strings and provide a None protection to ensure string
        comparisons work as expected. Also replace underscores with
        spaces.
        """
        return None if str_value is None else str_value.replace('_', ' ').lower()
