#!/usr/bin/env python
#pylint: disable=import-error
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
    identity_match_threshold = 2

    # Minimal number of data elements in a client content worksheet
    # required for creating a destination (reporting) worksheet.
    min_required_content_ws_columns = 3

    # Default country code for the phone number format.
    default_country_code = '1'

    # Default area code for the phone number format.
    default_area_code = '808'

    """
    DED Settings
    """
    # Required DED column headings.
    col_headings = [
        'Content DE Name',
        'Content DE Type',
        'Dest WS',
        'Dest DE Name',
        'Dest DE Format',
    ]
    de_name_col_idx = 0
    de_type_col_idx = 1
    dest_ws_col_idx = 2
    dest_de_name_col_idx = 3
    dest_de_format_col_idx = 4

    # Valid data element types.
    fragment_de_type = 'fragment'
    identifier_de_type = 'identifier'
    unit_test_de_type = 'unittestdet'

    # Valid data element formats.
    date_format = 'date'
    name_format = 'name'
    phone_format = 'phone'

    # Valid data element types list.
    valid_de_types = [
        identifier_de_type,
        fragment_de_type,
        unit_test_de_type,
    ]

    # Valid data element formats list.
    valid_de_formats = [
        date_format,
        name_format,
        phone_format,
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
            country_code = self.default_country_code

        if area_code is None:
            area_code = self.default_area_code

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
