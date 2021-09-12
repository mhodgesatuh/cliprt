#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_identity_registry import ClientIdentityRegistry
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry

class ClientIdentityRegistryTest:
    """
    Client identitly registry unit test harness.
    """
    # Dependencies
    dest_ws_reg = DestinationWorksheetsRegistry()

    # Test data
    client_id_reg = ClientIdentityRegistry(dest_ws_reg)

    def init_test(self):
        """
        Unit test
        """
        assert self.client_id_reg.get_next_client_idno() == 1000

    def create_identity_test(self):
        """
        Unit test
        """
        client_identity = self.client_id_reg.create_identity()
        client_id = client_identity.client_idno
        assert self.client_id_reg.client_id_list[client_id] == client_identity
        
    def get_identity_by_idno_test(self):
        """
        Unit test
        """
        client_identity = self.client_id_reg.create_identity()
        client_id = client_identity.client_idno
        assert self.client_id_reg.get_identity_by_idno(client_id) == client_identity
        assert self.client_id_reg.get_identity_by_idno(9999) == None
