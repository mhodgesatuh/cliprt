#!/usr/bin/env python
#pylint: disable=too-many-arguments
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from cliprt.classes.destination_worksheet import DestinationWorksheet

class DestinationWorksheetsRegistry:
    """
    The registry of destination worksheets is created when the DED is
    created and provides the list of destinations worksheets to be
    populated for reporting purposes.
    """
    def __init__(self):
        """
        Prepare a new registry for tracking the destination worksheets.
        """
        # Class attributes.
        self.dest_ws_by_ind_list = {}
        self.dest_ws_list = {}
        self.dest_ws_names = []

    def add_de_name(self, ws_ind, de_name, col_idx):
        """
        Add a new data element to the worksheet and update the column
        headings.
        """
        self.dest_ws_by_ind_list[ws_ind].add_de_name(de_name, col_idx)

    def add_ws(self, cliprt_wb, ws_ind):
        """
        As each destination worksheet is discovered add it to the
        destination worksheet repository.
        """
        if ws_ind in self.dest_ws_by_ind_list:
            return

        self.dest_ws_by_ind_list[ws_ind] = DestinationWorksheet(cliprt_wb, ws_ind)
        self.dest_ws_list[ws_ind] = self.dest_ws_by_ind_list[ws_ind].cliprt_ws_name

        # Update the list of destination worksheet names.
        # Later will need to skip these while processing the
        # data content worksheets.
        self.dest_ws_names.append(self.dest_ws_by_ind_list[ws_ind].cliprt_ws_name)

    def get_next_col_idx(self, ws_ind):
        """
        Return the next available column index for the requested
        worksheet.
        """
        return self.dest_ws_by_ind_list[ws_ind].get_next_col_idx()

    def prep_worksheets(self):
        """
        Create or reset the destination worksheet in preparation for the
        next round of reporting.
        """
        for ws_ind_dest_ws in self.dest_ws_by_ind_list.items():
            dest_ws = ws_ind_dest_ws[1]
            dest_ws.update_column_headings()
        #for ws_ind, dest_ws in self.dest_ws_by_ind_list.items():
        #    dest_ws.update_column_headings()

    def update_dest_ws_cell(self,
                            dest_ws_ind,
                            row_idx, col_idx,
                            cell_data,
                            data_format=None):
        """
        Update the specified cell in the specified destination worksheet.
        """
        self.dest_ws_by_ind_list[dest_ws_ind].update_cell(
            row_idx,
            col_idx,
            cell_data,
            data_format
        )
