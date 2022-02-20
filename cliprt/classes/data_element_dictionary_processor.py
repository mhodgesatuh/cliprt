#!/usr/bin/env python
#pylint: disable=too-many-instance-attributes
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from cliprt.classes.cliprt_settings import CliprtSettings
from cliprt.classes.data_element import DataElement
from cliprt.classes.message_registry import MessageRegistry

class DataElementDictionaryProcessor:
    """
    Process the data element worksheet and create the data element
    dictionary.
    """
    def __init__(self, wb, ws, dest_ws_registry):
        """
        Read the date element dictionary worksheet and hydrate the DED.
        """
        # Dependency injections.
        self.dest_ws_reg = dest_ws_registry

        # Class attributes.
        self.settings = CliprtSettings()
        self.de_fragments_list = {}
        self.ded = {}
        self.ded_hydrated = False
        self.cliprt = MessageRegistry()
        self.wb = wb
        self.ws = ws

    def ded_is_hydrated(self):
        """
        Indicsate whether or not the DED is hydrated.
        """
        return self.ded_hydrated

    def get_tuple_index(self, de_name, de_type, de_type_str):
        """
        Parse "type=n" entries to get the type index.
        """
        for tuple_info in self.util_make_list(de_type_str):

            if not '=' in tuple_info:
                # throw an error
                raise Exception(self.cliprt.msg(3210).format(
                    de_name,
                    de_type_str,
                    de_type
                ))

            tuple_parts = tuple_info.split('=', 1)
            if not tuple_parts[0] == de_type:
                # throw an error
                raise Exception(self.cliprt.msg(3217).format(
                    de_name,
                    de_type_str,
                    de_type
                ))
            if not tuple_parts[1].isdigit():
                # Fatal error
                raise Exception(self.cliprt.msg(3210).format(
                    de_name,
                    de_type_str,
                    de_type
                ))

            # Return the index value.
            return tuple_parts[1]

    def hydrate_ded(self):
        """
        Process the data Element worksheet and the report configuration
        and prepare the DED to be used for processing the client data
        worksheets and creating the destination reports.
        """
        if self.ded_is_hydrated():
            # It is already hydrated.
            return True

        # Determine column indicies for the required DED columns.
        # Ensure that all the required DED columns are provided.
        col_headings = self.read_col_headings()

        self.hydrate_ded_by_de(col_headings)
        self.hydrate_ded_by_dest_de(col_headings)
        self.hydrate_ded_by_dest_de_format(col_headings)
        self.hydrate_ded_by_de_type(col_headings)
        self.hydration_validation()

        # Success: the user-configured DED was processed.
        self.ded_hydrated = True
        return True

    def hydrate_ded_by_de(self, col_headings):
        """
        Data Element - specifies the data element name.
        Dest WS - specifies a 2-3 character reference value for each
            report destination, e.g.: fb for FaceBook.  Can be
            multivalued (comma delimited).
        """
        # Get the DED worksheet column of data element names.
        col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DE_NAME_COL_IDX]]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the data element name and associated
        # destination worksheet indicator and save to the DED.
        for de_cell in de_column:
            if de_cell.value is None:
                raise Exception(
                    self.cliprt.msg(3150).format(self.ws.title, de_cell.coordinate)
                )

            # Ensure values used for comparisons are shifted to
            # lowercase to reduce sensitivity to typos in the DED.
            de_name = self.settings.str_normalize(de_cell.value)
            if not de_name in self.ded:
                # Update the DED.
                self.ded[de_name] = DataElement(de_name, self.ded)

            # If destination worksheet indicators are specified, save
            # them to the DED.
            col_idx = col_headings[
                self.settings.COL_HEADINGS[self.settings.DEST_WS_COL_IDX]
            ]
            dest_ws_cell = self.ws.cell(row=de_cell.row, column=col_idx)
            if dest_ws_cell.value is None:
                continue
            for ws_dest_ind in self.util_make_list(dest_ws_cell.value):
                # Update the DED.
                self.process_dest_ind(de_name, ws_dest_ind)

    def hydrate_ded_by_dest_de(self, col_headings):
        """
        Dest Element - maps the content data element to a different
            data element in the report (not multivalued).
        """
        # Get the DED worksheet column of destination data element
        # names.
        col_idx = col_headings[
            self.settings.COL_HEADINGS[self.settings.DEST_DE_NAME_COL_IDX]
        ]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the destination data element name and save
        # to the DED.
        for dest_de_cell in de_column:
            if dest_de_cell.value is None:
                continue

            # Add the destination data element name and its information to the data
            # element dictionary.
            dest_de_name = self.settings.str_normalize(dest_de_cell.value)

            DE_NAME_COL_IDX = col_headings[
                self.settings.COL_HEADINGS[self.settings.DE_NAME_COL_IDX]
            ]
            de_cell = self.ws.cell(row=dest_de_cell.row, column=DE_NAME_COL_IDX)
            de_name = self.settings.str_normalize(de_cell.value)

            # Update the DED.
            self.ded[de_name].set_dest_de_name(dest_de_name)

    def hydrate_ded_by_dest_de_format(self, col_headings):
        """
        DE Format:
            1. date, name, phone: any of which will be used to help
                with the output format of the raw content data.  These
                are mutually exclusive.
        """
        # Get the DED worksheet column of destination data element
        # formats.
        col_idx = col_headings[
            self.settings.COL_HEADINGS[self.settings.DEST_DE_FORMAT_COL_IDX]
        ]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the destination data element name and save
        # to the DED.
        for de_format_cell in de_column:
            if de_format_cell.value is None:
                continue

            DE_NAME_COL_IDX = col_headings[
                self.settings.COL_HEADINGS[self.settings.DE_NAME_COL_IDX]
            ]
            de_cell = self.ws.cell(row=de_format_cell.row, column=DE_NAME_COL_IDX)
            de_name = self.settings.str_normalize(de_cell.value)

            dest_de_format = self.settings.str_normalize(de_format_cell.value)
            if not dest_de_format is None:
                self.process_dest_de_format(de_name, dest_de_format)

    def hydrate_ded_by_de_type(self, col_headings):
        """
        DE Type - includes the following, which are mutually exclusive:
            1. "identifier" to indicate that the content data will
                also be used for identity matching.
            2. "fragemnt=n" to indicate that content data needs to be
                combined into a single report destination value, e.g.:
                map first name and last name to a full name value at
                the report destination.
        """
        # Get the DED worksheet column of data element types.
        col_idx = col_headings[
            self.settings.COL_HEADINGS[self.settings.DE_TYPE_COL_IDX]
        ]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the destination data element name and save
        # to the DED.
        for de_format_cell in de_column:
            if de_format_cell.value is None:
                continue

            DE_NAME_COL_IDX = col_headings[
                self.settings.COL_HEADINGS[self.settings.DE_NAME_COL_IDX]
            ]
            de_cell = self.ws.cell(row=de_format_cell.row, column=DE_NAME_COL_IDX)
            de_name = self.settings.str_normalize(de_cell.value)

            dest_de_type = self.settings.str_normalize(de_format_cell.value)
            if not dest_de_type is None:
                self.process_de_type(de_name, dest_de_type)

    def hydration_validation(self):
        """
        Valid the DED elements to ensure the user input is correct and
        complete.
        """
        identifier_cnt = 0

        for de_name, de in self.ded.items():

            if de.is_identifier:
                identifier_cnt += 1

            if not de.dest_de_name is None and ',' in de.dest_de_name:
                raise Exception(self.cliprt.msg(3170).format(de_name, de.dest_de_name))

            if de.has_dest_ws() and not de.dest_de_name is None:
                raise Exception(self.cliprt.msg(3204).format(de_name))

            if not de.dest_de_name is None and not de.dest_de_name in self.ded:
                raise Exception(self.cliprt.msg(3207).format(de.dest_de_name))

            if de.is_fragment and\
                not de.dest_de_name is None and\
                self.ded[de.dest_de_name].is_remapped:
                raise Exception(self.cliprt.msg(3212).format(de.dest_de_name, de_name))

            if de.is_fragment and de.dest_de_name is None:
                raise Exception(self.cliprt.msg(3214).format(de_name))

            if de.is_fragment and de.dest_de_name is None:
                raise Exception(self.cliprt.msg(3216).format(de_name))

            if de.is_identifier and not de.dest_de_name is None:
                raise Exception(self.cliprt.msg(3226).format(de.dest_de_name, de_name))

            if not de.has_dest_ws() and de.dest_de_name is None:
                raise Exception(self.cliprt.msg(3232).format(de_name))

            # Dest_de must reference a DE with a defined dest_ws
            if not de.dest_de_name is None and not self.ded[de.dest_de_name].has_dest_ws():
                raise Exception(self.cliprt.msg(3238).format(de.dest_de_name, de_name))

        if identifier_cnt == 0:
            raise Exception(self.cliprt.msg(3229))

        return True

    def preconfig_ded_worksheet(self, de_names):
        """
        Preconfigure a fresh DED worksheet.
        """
        # Add the required DED column headings.
        col_idx = 1
        for col_heading in self.settings.COL_HEADINGS:
            self.ws.cell(1, col_idx, value=col_heading)
            col_idx += 1
        # Add the list of data element names to the first column.
        row_idx = 2
        for de_name in de_names:
            self.ws.cell(row_idx, 1, value=de_name)
            row_idx += 1

    def print_report(self):
        """
        Print the DED contents to the console.
        """
        if not self.ded_is_hydrated():
            self.hydrate_ded()
        print()
        print("----------------------------------------")
        print("Report: Client Data Elemement Dictionary")
        print('> ded[]')
        print("----------------------------------------")
        for de_name, de_instance in self.ded.items():
            print(f'{de_name} : {de_instance}')
        print()

    def process_dest_ind(self, de_name, ws_dest_ind):
        """
        For each data element more than one destination worksheet may be
        specified in the DED worksheet.
        """
        if not ws_dest_ind in self.dest_ws_reg.dest_ws_by_ind_list:
            # Autodetect and save new destination indicators.
            self.dest_ws_reg.add_ws(self.wb, ws_dest_ind)

        # Each column heading is assigned the next available column.
        # Increment the index of the last data element column of the
        # specified destination worksheet.
        dest_col_idx = self.dest_ws_reg.get_next_col_idx(ws_dest_ind)
        self.ded[de_name].add_dest_ws_ind(ws_dest_ind, dest_col_idx)

        # This will be used to create the column headings for each
        # of the destination worksheets.
        self.dest_ws_reg.add_de_name(ws_dest_ind, de_name, dest_col_idx)

    def process_dest_de_format(self, de_name, dest_de_format):
        """
        Process the destination data element format destination and
        update the data element instance accordingly.
        """
        # Validate the destination data element format designater.
        if not dest_de_format in self.settings.VALID_DE_FORMATS:
            # Fatal error, invalid destination format
            raise Exception(self.cliprt.msg(3217).format(
                dest_de_format,
                de_name,
                self.settings.VALID_DE_FORMATS))

        # Save the destintion format to the DED.
        self.ded[de_name].set_dest_de_format(dest_de_format)
        return True

    def process_de_type(self, de_name, de_type):
        """
        Process the destination data element type destination and update
        the data instance accordingly if designations are found.
        """
        if ',' in de_type:
            raise Exception(self.cliprt.msg(3215).format(de_type, de_name))

        # Check for identifier type.
        if de_type == self.settings.IDENTIFIER_DE_TYPE:
            self.ded[de_name].set_to_identifier()
            return True

        # Check for fragment type.
        if self.settings.FRAGMENT_DE_TYPE in de_type:
            frag_idx = self.get_tuple_index(
                de_name,
                self.settings.FRAGMENT_DE_TYPE,
                de_type)
            self.de_fragments_list[de_name] = frag_idx
            self.ded[de_name].set_to_fragment(self.de_fragments_list[de_name])
            return True

        if not de_type in self.settings.VALID_DE_TYPES:
            raise Exception(self.cliprt.msg(3218).format(
                de_type,
                de_name,
                self.settings.VALID_DE_TYPES))
        return True

    def read_col_headings(self, evaluate_only=False):
        """
        Get the column headings and retain the column indices.
        """
        if self.ws is None:
            return False

        col_headings = {}
        for cell in self.ws[self.ws.min_row]:
            col_headings[cell.value] = cell.col_idx

        # Ensure that all of the required named columns are available.
        for ded_col_heading in self.settings.COL_HEADINGS:
            if ded_col_heading not in col_headings:
                if evaluate_only:
                    # No fatal error to be thrown.
                    return False
                # Fatal error
                raise Exception(self.cliprt.msg(3200).format(
                    ded_col_heading,
                    self.ws.title))
        return col_headings

    @staticmethod
    def util_make_list(str_value):
        """
        Convert a comma-delimited string to a list.  These lists are
        usually provided by the user in the DED configuration.
        """
        return None if str_value is None else str_value.replace(' ', '').split(',')
