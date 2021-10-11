#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from datetime import *
from cliprt.classes.cliprt_settings import CliprtSettings
from cliprt.classes.data_element import DataElement
from cliprt.classes.message_registry import MessageRegistry

class DataElementDictionaryProcessor:

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
        """
        return self.ded_hydrated

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
        # > col_headings[col_name] = col_idx
        col_headings = self.read_col_headings()

        self.hydrate_ded_by_de(col_headings)
        self.hydrate_ded_by_dest_de(col_headings)
        self.hydrate_ded_by_de_format(col_headings)
        self.hydration_validation()

        # Success: the user configured DED was processed.
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
        col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DE_COL_IDX]]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the data element name and associated
        # destination worksheet indicator and save to the DED.
        for de_cell in de_column:
            if de_cell.value == None:
                raise Exception(self.cliprt.msg(3150).format(self.ws.title, de_cell.coordinate))

            # Ensure values used for comparisons are shifted to
            # lowercase to reduce sensitivity to typos in the DED.
            de_name = self.settings.str_normalize(de_cell.value)
            if not de_name in self.ded:
                # Update the DED.
                self.ded[de_name] = DataElement(de_name, self.ded)

            # If destination worksheet indicators are specified, save
            # them to the DED.
            col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DEST_WS_COL_IDX]]
            dest_ws_cell = self.ws.cell(row=de_cell.row, column=col_idx)
            if dest_ws_cell.value == None:
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
        col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DEST_DE_COL_IDX]]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the destination data element name and save
        # to the DED.
        for dest_de_cell in de_column:
            if dest_de_cell.value == None:
                continue

            # Add the destination data element name and its information to the data
            # element dictionary.
            dest_de_name = self.settings.str_normalize(dest_de_cell.value)

            de_col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DE_COL_IDX]]
            de_cell = self.ws.cell(row=dest_de_cell.row, column=de_col_idx)
            de_name = self.settings.str_normalize(de_cell.value)

            # Update the DED.
            self.ded[de_name].set_dest_de_name(dest_de_name)

    def hydrate_ded_by_de_format(self, col_headings):
        """
        DE Format - is overloaded with the following:
            1. date, name, phone: any of which will be used to help
                with the output format of the raw content data.
            2. "identifier" to indicate that the content data will
                also be used for identity matching.
            3. "fragemnt=n" to indicate that content data needs to be
                combined into a single report destination value, e.g.:
                map first name and last name to a full name value at
                the report destination.
        """
        # Get the DED worksheet column of data element formats.
        col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DE_FORMAT_COL_IDX]]
        ws_columns = self.ws.iter_cols(
            min_col=col_idx,
            max_col=col_idx,
            min_row=self.ws.min_row+1)
        de_column = list(ws_columns)[0]

        # From each row get the destination data element name and save
        # to the DED.
        for de_format_cell in de_column:
            if de_format_cell.value == None:
                continue

            de_col_idx = col_headings[self.settings.COL_HEADINGS[self.settings.DE_COL_IDX]]
            de_cell = self.ws.cell(row=de_format_cell.row, column=de_col_idx)
            de_name = self.settings.str_normalize(de_cell.value)

            dest_de_format_str = self.settings.str_normalize(de_format_cell.value)
            if not dest_de_format_str == None:
                dest_de_format_list = self.parse_dest_de_format_str(de_name, dest_de_format_str)
                for dest_de_format in dest_de_format_list:
                    self.process_dest_de_format(de_name, dest_de_format)

    def hydration_validation(self):
        """
        Valid the DED elements to ensure the user input is correct and
        complete.
        """
        identifier_cnt = 0

        for de_name, de in self.ded.items():

            if de.is_identifier:
                identifier_cnt += 1

            if not de.dest_de_name == None and ',' in de.dest_de_name:
                raise Exception(self.cliprt.msg(3170).format(de_name, de.dest_de_name))

            if de.has_dest_ws() and not de.dest_de_name == None:
                raise Exception(self.cliprt.msg(3204).format(de_name))

            if not de.dest_de_name == None and not de.dest_de_name in self.ded:
                raise Exception(self.cliprt.msg(3207).format(de.dest_de_name))

            if de.is_fragment and not de.dest_de_name == None and self.ded[de.dest_de_name].is_remapped:
                raise Exception(self.cliprt.msg(3212).format(de.dest_de_name, de_name))

            if de.is_fragment and de.dest_de_name == None:
                raise Exception(self.cliprt.msg(3214).format(de_name))

            if de.is_identifier and de.is_fragment:
                raise Exception(self.cliprt.msg(3215).format(de_name))

            if de.is_identifier and not de.dest_de_name == None:
                raise Exception(self.cliprt.msg(3226).format(de.dest_de_name, de_name))

            if not de.has_dest_ws() and de.dest_de_name == None:
                raise Exception(self.cliprt.msg(3232).format(de_name))

            # Dest_de must reference a DE with a defined dest_ws
            if not de.dest_de_name == None and not self.ded[de.dest_de_name].has_dest_ws():
                raise Exception(self.cliprt.msg(3238).format(de.dest_de_name, de_name))

        if identifier_cnt == 0:
            raise Exception(self.cliprt.msg(3229))

        return True

    def parse_dest_de_format_str(self, de_name, dest_de_format_str):
        """
        Preprocess the raw destination format list and parse "fragment"
        entries to get the fragment index.
        """
        dest_de_format_list = []

        for dest_de_format in self.util_make_list(dest_de_format_str):

            # Determine if the destination format needs to be parsed.
            if '=' in dest_de_format:

                # Parse the destination format from the assigned index.
                dest_de_format_part = dest_de_format.split('=',1)

                # Parsed, this is the clean destination format.
                dest_de_format = dest_de_format_part[0]

                # Currently the assigned index is only relevant for
                # a "fragment", the rest are ignored.
                if dest_de_format == self.settings.FRAGMENT_DESIGNATION:
                    if not dest_de_format_part[1].isdigit():
                        # Fatal error
                        raise Exception(self.cliprt.msg(3210).format(de_name, self.ws.title))

                    # Save the fragment index for later.
                    self.de_fragments_list[de_name] = int(dest_de_format_part[1])

            # Add the clean destination format to the list.
            dest_de_format_list.append(dest_de_format)

        return dest_de_format_list

    def preconfig_ded_worksheet(self, de_names):
        """
        Preconfigure a fresh DED worksheet.
        """
        # Add the required DED column headings.
        col_idx = 1
        for col_heading in self.settings.COL_HEADINGS:
            self.ws.cell(1, col_idx, value=col_heading)
            col_idx+=1
        # Add the list of data element names to the first column.
        row_idx = 2
        for de_name in de_names:
            self.ws.cell(row_idx, 1, value=de_name)
            row_idx+=1

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
            print('{} : {}'.format(de_name, de_instance))
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
        The destination format is overloaded with data formatting
        information as well as identifier and fragment attribute
        designations. Parse the destination format data and update
        the data element instance accordingly if designations are
        found.
        """
        # Validate the destination format designater.
        if not dest_de_format in self.settings.VALID_DE_FORMATS:
            # Fatal error, invalid destination format
            raise Exception(self.cliprt.msg(3217).format(dest_de_format, de_name, self.settings.VALID_DE_FORMATS))

        # Check for the overload identifier and fragment designaters.
        if dest_de_format == self.settings.IDENTIFIER_DESIGNATION: # todo: is this right?
            self.ded[de_name].set_to_identifier()
        elif dest_de_format == self.settings.FRAGMENT_DESIGNATION:
            if de_name in self.de_fragments_list:
                self.ded[de_name].set_to_fragment(self.de_fragments_list[de_name])
            else:
                # Fatal error, invalid destination format
                raise Exception(self.cliprt.msg(3220).format(dest_de_format, de_name, self.settings.VALID_DE_FORMATS))
        else:
            # Save the destintion format designater to the DED.
            self.ded[de_name].set_dest_de_format(dest_de_format)

    def read_col_headings(self, evaluate_only = False):
        """
        Get the column headings and retain the column indices.
        """
        if self.ws == None:
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
                raise Exception(self.cliprt.msg(3200).format(ded_col_heading, self.ws.title))
        return col_headings

    def util_make_list(self, str_value):
        """
        Convert a comma-delimited string to a list.  These lists are
        usually provided by the user in the DED configuration.
        """
        return None if str_value == None else str_value.replace(' ','').split(',')