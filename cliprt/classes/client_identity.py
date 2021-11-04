#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class ClientIdentity:
    """
    Each client is assigned a unique identifier that is used to merge
    content date in the report destination worksheets.  Tracking of the
    target row for each destination worksheet is required in order to
    successfully merge data.
    """
    def __init__(self, client_idno, dest_ws_registry):
        """
        Create a new identity.  The identity registry is an injected
        service that will provide the next available id.  An identity
        may have one or more identifiers that in combination are
        uniquely associated with this particular identity.
        """
        # Class attributes.
        self.client_idno = client_idno
        self.dest_ws = {}

        # Initializations.
        self.add_dest_ws_info(dest_ws_registry.dest_ws_by_ind_list)

    def add_dest_ws_info(self, dest_ws_by_ind_list):
        """
        Each client identifier is assigned its own row in each of the
        destination worksheets.
        """
        for dest_ws_ind, dest_ws in dest_ws_by_ind_list.items():
            row_idx = dest_ws.get_next_row_idx()
            self.dest_ws[dest_ws_ind] = row_idx

    def get_row_idx(self, dest_ws_ind):
        """
        Get the target row for merging client data.
        """
        return self.dest_ws[dest_ws_ind]
