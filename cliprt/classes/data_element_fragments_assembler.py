#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class DataElementFragmentsAssembler:
    """
    Collect the data element fragments for a data element.  Once all of
    the fragments are provided the assembled value of the data element
    is available.  For example, the "name" data element might need to be
    assembled from the "first name" and "last name" data elements.  The
    order of the fragments is needed for a correct assembly.
    """

    def __init__(self, de_name):
        """
        Specify the data element name to be assembled.
        """
        # Class attributes.
        self.assembled_de_name = de_name
        self.fragments_col_indicies = {}
        self.fragments_values = {}

    def __str__(self):
        """
        Display the contents of the assembler for reporting purposes.
        """
        ret_val = ''
        delim = ', '
        for frag_idx, frag_de in self.fragments_col_indicies.items():
            ret_val += f"{delim}{{'{frag_idx}': '{frag_de}'}}"
        return f"'{self.assembled_de_name}': {{{ret_val[len(delim):]}}}"

    def add_fragment_col_index(self, fragment_de_name, ws_col):
        """
        Add another data element fragment to the assembler.  Its column
        index will later be used to retrieve and assemble the values.
        """
        if not fragment_de_name in self.fragments_col_indicies:
            self.fragments_col_indicies[fragment_de_name] = ws_col

    def add_fragment_value(self, fragment_idx, fragment_value):
        """
        Add another data element fragment to the assembler.
        """
        self.fragments_values[fragment_idx] = fragment_value

    def assembled_value(self):
        """
        Assemble the value of the data element.
        """
        ret_value = ''
        for i in sorted(self.fragments_values):
            ret_value += f' {self.fragments_values[i]}'
        return ret_value.strip()
