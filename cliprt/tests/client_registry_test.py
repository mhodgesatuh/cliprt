#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2021 Michael Hodges
"""
from cliprt.classes.client_registry import ClientRegistry
from cliprt.classes.destination_worksheets_registry import DestinationWorksheetsRegistry

class ClientRegistryTest:
    """
    Client identitly registry unit test harness.
    """
    dest_ws_reg = DestinationWorksheetsRegistry()

    # Test data
    client_reg = ClientRegistry(dest_ws_reg)

    def create_identity_test(self):
        """
        Unit test
        """
        client_identity = self.client_reg.create_identity()
        client_id = client_identity.client_idno
        assert self.client_reg.client_id_list[client_id] == client_identity

    def get_identity_by_idno_test(self):
        """
        Unit test
        """
        client_identity = self.client_reg.create_identity()
        client_id = client_identity.client_idno
        assert self.client_reg.get_identity_by_idno(client_id) == client_identity
        assert self.client_reg.get_identity_by_idno(9999) is None

    def init_test(self):
        """
        Unit test
        """
        client_reg = ClientRegistry(self.dest_ws_reg)
        assert client_reg.get_next_client_idno() is 1000
