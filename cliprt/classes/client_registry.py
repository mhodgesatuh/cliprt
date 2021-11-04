#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
from cliprt.classes.client_identity import ClientIdentity

class ClientRegistry:
    """
    The client identifier registry keeps track of all client id's and
    provide the next available client id number when a new client
    identifier is added to the registry.
    """
    def __init__(self, dest_ws_registry, starting_client_idno=1000):
        """
        Create a new identitity registry and set the value of the initial
        client id number.
        """
        # Dependency injections.
        self.dest_ws_reg = dest_ws_registry

        # Class attributes.
        self.client_id_list = {}
        self.next_client_idno = starting_client_idno

    def create_identity(self):
        """
        There should be one unique identity for each client.  A client
        id is a unique number that is associated with each client.
        Creation of an identity automatically adds it to the list in
        the registry.
        """
        client_idno = self.get_next_client_idno()
        identity = ClientIdentity(client_idno, self.dest_ws_reg)
        self.client_id_list[client_idno] = identity
        return identity

    def get_identity_by_idno(self, client_idno):
        """
        Return the client id.
        """
        if client_idno in self.client_id_list:
            return self.client_id_list[client_idno]
        return None

    def get_next_client_idno(self):
        """
        The client identity registry keeps track of the next available
        client id number.  Once served, the regisrty is updated for the
        next request for a client id number.
        """
        client_idno = self.next_client_idno
        self.next_client_idno += 1
        return client_idno
