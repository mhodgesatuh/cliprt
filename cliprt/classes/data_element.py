#!/usr/bin/env python
#pylint: disable=too-many-instance-attributes
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2022 Michael Hodges
"""
class DataElement:
    """
    Each column of each client worksheet is considered to be a data
    element.  A single data element may be repeated across one or more
    client worksheets.
    """
    def __init__(self, name, ded_processor):
        """
        Prepare a new data element.
        """
        # Dependency injections.
        self.ded_processor = ded_processor

        # Class attributes.
        self.dest_de_format = None
        self.dest_de_name = None
        self.dest_ws_info = {}
        self.fragment_idx = None
        self.is_content = True
        self.is_fragment = False
        self.fragment_idx = int()
        self.is_identifier = False
        self.is_remapped = False
        self.name = name

    def __str__(self):
        """
        Display the contents of the data element for reporting purposes.
        """
        i = 0
        str_val = {}
        if self.is_remapped:
            str_val[i] = self.util_format_dict_output(
                'dest_de_name',
                self.dest_de_name
                )
            i += 1
        if self.is_content:
            str_val[i] = 'is_content'
            i += 1
        if self.is_identifier:
            str_val[i] = 'is_identifier'
            i += 1
        if self.is_fragment:
            str_val[i] = self.util_format_dict_output(
                'fragment_idx',
                self.fragment_idx
                )
            i += 1
        if self.dest_de_format is not None:
            str_val[i] = self.util_format_dict_output(
                'dest_de_format',
                self.dest_de_format
                )
            i += 1
        for dest_ws_ind, dest_info in self.dest_ws_info.items():
            str_val[i] = self.util_format_dict_output(
                dest_ws_ind,
                dest_info
                )
            i += 1
        ret_val = ''
        i = 0
        delim = ', '
        while i < len(str_val):
            # Insert a delimitor between each attribute.
            ret_val += f'{delim}{str_val[i]}'
            i += 1
        # Remove leading delimitor.
        return ret_val[len(delim):]

    def add_dest_ws_ind(self, dest_ws_ind, dest_col_idx):
        """
        Each content data value is matched to a column for each
        destination report. Example data:
        """
        if not dest_ws_ind in self.dest_ws_info:
            self.dest_ws_info[dest_ws_ind] = {'col_idx': dest_col_idx}

    def get_col_by_dest_ws_ind(self, dest_ws_ind):
        """
        Each content data value may be matched to a column for each
        destination report.  Depends on how the DED is configured for
        reporting purposes.
        """
        if not dest_ws_ind in self.dest_ws_info:
            # There is no destination worksheet specified for this data
            # eleement.
            return False
        return self.dest_ws_info[dest_ws_ind]['col_idx']

    def get_identifier_type(self):
        """
        Select data elements are tagged as identifiers.  Remapped
        identifiers are typed by their destination data elements.
        The number of unique types of identifiers is info used for
        determining identity matches.
        """
        return self.dest_de_name if self.is_remapped else self.name

    def is_mapped_to_dest_ws(self, dest_ws_ind):
        """
        Each data element to be included in the report is mapped to one
        or more destination reports.
        """
        return dest_ws_ind in self.dest_ws_info

    def has_dest_ws(self):
        """
        Determine if the data element has at least one destination worksheet.
        """
        return len(self.dest_ws_info) > 0

    def set_dest_de_name(self, de_name):
        """
        This data element will be remapped to the designated data
        element on the destination report worksheets.  Set the
        destination data element name.
        """
        self.dest_de_name = de_name
        self.is_remapped = True

    def set_dest_de_format(self, de_format):
        """
        The destination data element formatting will determine the final
        format of the data element when it is saved to the spreadsheet
        cell.
        """
        self.dest_de_format = de_format

    def set_to_fragment(self, fragment_idx):
        """
        Note that a data element is either content or a fragment.  It
        must be one or the other.
        """
        self.fragment_idx = fragment_idx
        self.is_content = False
        self.is_fragment = True

    def set_to_identifier(self):
        """
        If the data element is an identifier unset the content setting
        so that it is only processed as an identifier.
        """
        self.is_identifier = True
        self.is_content = False

    @staticmethod
    def util_format_dict_output(key, val):
        """
        Format output as "{'key': val}"
        """
        if isinstance(val, str):
            output_format = "{{'{}': '{}'}}"
        else:
            output_format = "{{'{}': {}}}"
        return output_format.format(key, val, type(val))
