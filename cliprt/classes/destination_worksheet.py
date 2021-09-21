#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from cliprt.classes.data_element_dictionary_settings import DataElementDictionarySettings

class DestinationWorksheet:
    """
    Prepare a new report destination worksheet.  Create it if it does
    not exist, and reset it if it does so that it is reay for the next
    reporting request.
    """
    DEST_WS_NAME_PREFIX = 'comm_report_for_'

    def __init__(self, wb, ws_ind):
        """
        Start a new destination worksheet, or reset an existing one
        if it has been left behind from a previous report creation
        request.
        """
        # Class attributes.
        self.ded_settings = DataElementDictionarySettings()
        self.dest_de_list = {}
        self.dest_ind = ws_ind
        self.first_row_idx = 1
        self.next_col_idx = 1
        self.next_row_idx = 2
        self.ws = None
        self.ws_name = self.DEST_WS_NAME_PREFIX + ws_ind

        if not self.ws_name in wb.sheetnames:
            self.ws = wb.create_sheet(title=self.ws_name)
        else:
            self.ws = wb[self.ws_name]
            self.reset()

    def add_de_name(self, de_name, col_idx):
        """
        Add a new data element to the worksheet and update the column
        headings.
        """
        self.dest_de_list[de_name] = col_idx
        self.ws.cell(self.first_row_idx, col_idx, value=de_name)

    def get_next_col_idx(self):
        """
        Continue adding each client's information to a new row in the
        report.
        """
        next_col_idx = self.next_col_idx
        self.next_col_idx+=1
        return next_col_idx

    def get_next_row_idx(self):
        """
        Continue adding each client's information to a new row in the
        report.
        """
        next_row_idx = self.next_row_idx
        self.next_row_idx+=1
        return next_row_idx

    def reset(self):
        """
        Delete all rows to make room for a new report.
        """
        row_cnt = self.ws.max_row - self.ws.min_row + 1
        self.ws.delete_rows(self.ws.min_row, amount=row_cnt)

    def update_cell(self, row_idx, col_idx, cell_data, data_format = None):
        """
        Determine if the destination cell already has a value in it add the new value to the
        using a comma delimitor.
        """
        if cell_data == None:
            # If there's no new data there's nothing to do.
            return True

        # Format the new cell data if a data format has been provided.
        if data_format == self.ded_settings.DATE_FORMAT:
            formatted_data = self.ded_settings.format_date(cell_data)
        elif data_format == self.ded_settings.NAME_FORMAT:
            formatted_data = self.ded_settings.format_name(cell_data)
        elif data_format == self.ded_settings.PHONE_FORMAT:
            formatted_data = self.ded_settings.format_phone(cell_data)
        else:
            formatted_data = str(cell_data)

        cell_value = self.ws.cell(row_idx, col_idx).value
        if cell_value == None:
            # Simply write the new cell data to an empty destination cell.
            self.ws.cell(row_idx, col_idx, value=formatted_data)
        elif formatted_data.lower() in cell_value.lower():
            # Don't save the same data twice.
            pass
        else:
            # Update the cell value.
            self.ws.cell(row_idx, col_idx, value='{}, {}'.format(cell_value, formatted_data))
        return True
        
    def update_column_headings(self):
        """
        Update the columns heads based on the information provided by 
        the DED.
        """
        for col_name, col_idx in self.dest_de_list.items():
            self.ws.cell(1, col_idx, value=col_name)