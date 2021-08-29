#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class ClientIdentifierRegistry:
    """
    Client identities are composed of a unique combination of multiple 
    client identifiers. A specific identifier may be shared by one or
    client identities, for example, a married couple sharing a single 
    email address.
    """    
    def __init__(self, client_id_registry):
        """
        Create a new client identity registry.
        """
        # Dependency injection.
        self.client_id_registry = client_id_registry

        # Class attributes.
        self.identifier_list = {}

    def add_identifier(self, identifier):
        """
        Add a new client identifier to the client identity registry and
        update the identifiers registry with the new client id info.
        """
        if not identifier.key in self.identifier_list.items():
            self.identifier_list[identifier.key] = identifier