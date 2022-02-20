#!/usr/bin/env python
#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-arguments
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from cliprt.classes.client_identity_resolver import ClientIdentityResolver
from cliprt.classes.cliprt_settings import CliprtSettings
from cliprt.classes.data_element_fragments_assembler import DataElementFragmentsAssembler\
        as FragAssembler
from cliprt.classes.identifier import Identifier
from cliprt.classes.message_registry import MessageRegistry

class ContentWorksheet:
    """
    Content worksheets contain client data.  Client data from multiple
    worksheets will be merged into the destination report worksheets.
    """
    # Flag the identifer column index as 'assembled' since there is no
    # single column associated with the identifier.
    ASSEMBLED_IDENTIFIER = '<n/a>'

    # Display progress interval size.
    PROGRESS_INCREMENT = 50

    def __init__(
            self,
            wb,
            ws_name,
            ded_processor,
            client_registry,
            identifier_registry,
            dest_ws_registry
        ):
        """
        Ready a content worksheet for processing.
        """
        # Dependency injections.
        self.ded_processor = ded_processor
        self.client_reg = client_registry
        self.identifier_reg = identifier_registry
        self.dest_ws_reg = dest_ws_registry
        self.settings = CliprtSettings()

        # Class attributes.
        self.content_cols = {}
        self.de_names = []
        self.ded = ded_processor.ded
        self.cliprt = MessageRegistry()
        self.frag_assembler_list = {}
        self.identifier_col_names = {}
        self.wb = wb
        self.ws = wb[ws_name]
        self.ws_name = ws_name

    def build_etl_map(self):
        """
        Build the destination data element ETL mappings.  These ETL
        mappings will provde exact instructions for mapping each
        content data element to each of the destination worksheets.
        """
        # Read the top row and build the ETL mappings to the destination
        # worksheets.  Also flag the identity and fragment columns for
        # special processing.
        ws_top_row = list(self.ws.iter_rows(
            min_row=self.ws.min_row,
            max_row=self.ws.min_row
            ))[0]
        for ws_cell in ws_top_row:

            if ws_cell.value is None:
                # Skip empty columns.
                continue

            ws_de_name = self.settings.str_normalize(ws_cell.value)
            if not ws_de_name in self.ded:
                # Skip this data element if it is not in the DED.
                continue

            # Determine what the destination data element will be.
            if self.ded[ws_de_name].is_remapped:
                # This is a remapping: a->b rather than a->a.
                # Note that fragments are always remapped: a+b->c.
                dest_de_name = self.ded[ws_de_name].dest_de_name
                dest_de = self.ded[dest_de_name]
            else:
                # This is a simple mapping: a->a.
                dest_de_name = ws_de_name
                dest_de = self.ded[ws_de_name]

            # ETL mapping.
            if not dest_de_name in self.de_names:
                self.de_names.append(dest_de_name)
            if self.ded[ws_de_name].is_fragment:
                # Add the content data element to the list of data
                # element fragment assemblers.
                if not dest_de_name in self.frag_assembler_list:
                    # Create a fragments assembler if needed.
                    self.frag_assembler_list[dest_de_name] = FragAssembler(dest_de_name)
                if not dest_de_name in self.identifier_col_names:
                    self.identifier_col_names[dest_de_name] = self.ASSEMBLED_IDENTIFIER
                # Add the new data element fragment to the assembler.
                self.frag_assembler_list[dest_de_name].add_fragment_col_index(
                    ws_de_name,
                    ws_cell.column
                    )
            elif self.ded[dest_de_name].is_identifier:
                # Ensure that individual fragments are not processed as
                # identifiers.
                self.identifier_col_names[ws_de_name] = ws_cell.column
            else:
                # If none of the above, it's content.
                self.content_cols[ws_cell.column] = ws_de_name

    def client_report(self, progress_reporting_is_disabled=False):
        """
        Create the destination report worksheets.
        """
        self.build_etl_map()
        if not progress_reporting_is_disabled:
            self.print_progress_report()

        if len(self.content_cols) + len(self.identifier_col_names) < \
                self.settings.MIN_REQUIRED_CONTENT_WS_COLUMNS:
            # Skip worksheets with insufficient data to report.
            if not progress_reporting_is_disabled:
                print(self.cliprt.msg(5000).format(self.ws_name))
            return False

        self.process_ws_rows(progress_reporting_is_disabled)
        return True

    def print_frag_assembler_list(self):
        """
        List the fragments.
        """
        ret_val = ''
        delim = ', '
        for de_name, frag_de in self.frag_assembler_list.items():
            ret_val += f'{delim}{ frag_de.__str__()}'
        return '[' + ret_val[len(delim):] + ']'


    def print_progress_report(self):
        """
        Display information about the worksheet.
        """
        print('--------')
        print(f'Worksheet currently in progress: {self.ws_name}')
        print(f'Rows of content to be processed: {self.ws.max_row}')
        print(f'DE Names     > ws_de_names     : {self.de_names}')
        print(f'DE Fragments > fragment_cols   : {self.print_frag_assembler_list()}')
        print(f'Identifiers  > identifier_cols : {self.identifier_col_names}')
        print(f'Content      > content_cols    : {self.content_cols}')
        print(f"Processing in progress         : {'-'*self.PROGRESS_INCREMENT}")
        print('                               : ', end='')

    def process_row_de_fragments(self, row_idx):
        """
        Collect the data element fragments in assemblers.
        """
        if len(self.frag_assembler_list) == 0:
            # There are no fragments to process.
            return False

        for dest_de_name, fragments_assembler in self.frag_assembler_list.items():
            # Get each data element fragment name, look up its worksheet
            # column index and get the fragment's value from the
            # worksheet row and save it to the assembler.
            for fragment_name, col_idx in fragments_assembler.fragments_col_indicies.items():
                # Get the data vslue from the appropriate worksheet
                # column.  Replace null strings with empty strings as
                # needed.
                frag_value = self.ws.cell(row_idx, col_idx).value \
                    if not self.ws.cell(row_idx, col_idx).value is None \
                    else ''
                # The DED has the fragment index.
                frag_idx = self.ded[fragment_name].fragment_idx
                # Provide the data value to the fragment assembler.
                self.frag_assembler_list[dest_de_name].add_fragment_value(frag_idx, frag_value)
        return True

    def process_row_de_identifiers(self, client_id_resolver, row_idx):
        """
        Process the identifiers for the current row.
        """
        if len(self.identifier_col_names) == 0:
            # Fatal error: identifiers are required since this is client
            # information.  Identifiers identify which client the data
            # belongs too.
            raise Exception(self.cliprt.msg(5012).format(self.wb.active.title))

        # Process the identifiers.
        for de_name, col_idx in self.identifier_col_names.items():
            if col_idx == self.ASSEMBLED_IDENTIFIER:
                de_value = self.frag_assembler_list[de_name].assembled_value()
            else:
                de_value = self.ws.cell(row_idx, col_idx).value
            identifier = Identifier(de_name, de_value, self.ded)
            client_id_resolver.save_identifier(identifier)

        # Resolve the client's identity.  None returned if there are no
        # useful identifiers provided for establishing an identity.
        identity = client_id_resolver.resolve_client_identity(
            self.settings.IDENTITY_MATCH_THRESHOLD
            )
        return identity

    def process_ws_rows(self, progress_reporting_is_disabled=False):
        """
        Copy the content worksheet information to the destination
        worksheet. Note that this worksheet would have been skipped
        if it has no content.
        """

        # The first row holds the column headings.
        row_idx = self.ws.min_row

        # Scale the progress bar update threshold.
        if self.ws.max_row > self.PROGRESS_INCREMENT:
            # Large content worksheets.
            progress_threshold = int(self.ws.max_row/self.PROGRESS_INCREMENT)
        else:
            # Small content worksheets.
            progress_threshold = 1

        # Process each row of the content worksheet.
        while row_idx < self.ws.max_row:
            row_idx += 1

            if not progress_reporting_is_disabled and row_idx % progress_threshold == 0:
                # Update the progress report indicator.
                print('x', end='')

            # First process the fragmented data elements columns and
            # assemble them, some of which may be identifiers.
            self.process_row_de_fragments(row_idx)

            # Process the identifiers in order to determine if this is
            # a new or a previously identified client.
            client_id_resolver = ClientIdentityResolver(
                self.client_reg,
                self.identifier_reg
            )
            identity = self.process_row_de_identifiers(
                client_id_resolver,
                row_idx
            )

            # Copy the matched identifiers values to the destination worksheet.
            for dest_ws_ind, dest_row_idx in identity.dest_ws.items():

                for identifier in client_id_resolver.identifiers_matched:
                    # Update the destination report worksheet.
                    dest_de_name = identifier.de_name
                    dest_col_idx = self.ded[dest_de_name].get_col_by_dest_ws_ind(dest_ws_ind)
                    if dest_col_idx is False:
                        # There is no destination worksheet specified
                        # for this data eleement.
                        continue
                    dest_de_value = identifier.de_value
                    dest_de_format = self.ded[dest_de_name].dest_de_format
                    self.dest_ws_reg.update_dest_ws_cell(
                        dest_ws_ind,
                        dest_row_idx,
                        dest_col_idx,
                        dest_de_value,
                        dest_de_format
                        )

                # Copy the content columns to the destination worksheet.
                for col_idx, dest_de_name in self.content_cols.items():
                    dest_de_value = self.ws.cell(row_idx, col_idx).value

                    if dest_de_value is None:
                        # Skip empty cells.
                        continue
                    if not self.ded[dest_de_name].is_mapped_to_dest_ws(dest_ws_ind):
                        # Not all content gets copied to all destination
                        # worksheets.
                        continue

                    # Update the destination report worksheet.
                    dest_col_idx = self.ded[dest_de_name].get_col_by_dest_ws_ind(dest_ws_ind)
                    dest_de_format = self.ded[dest_de_name].dest_de_format
                    self.dest_ws_reg.update_dest_ws_cell(
                        dest_ws_ind,
                        dest_row_idx,
                        dest_col_idx,
                        dest_de_value,
                        dest_de_format
                        )

                # Copy assembled content fragments to the destination
                # worksheet.
                for dest_de_name, frag_info in self.frag_assembler_list.items():

                    # Update the destination report worksheet.
                    dest_row_idx = identity.get_row_idx(dest_ws_ind)
                    dest_col_idx = self.ded[dest_de_name].get_col_by_dest_ws_ind(dest_ws_ind)
                    dest_de_value = frag_info.assembled_value()
                    dest_de_format = self.ded[dest_de_name].dest_de_format
                    self.dest_ws_reg.update_dest_ws_cell(
                        dest_ws_ind,
                        dest_row_idx,
                        dest_col_idx,
                        dest_de_value,
                        dest_de_format
                        )
        if not progress_reporting_is_disabled:
            # Output a new line to finish up the progress report.
            print()

        return True
