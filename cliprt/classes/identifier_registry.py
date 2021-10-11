#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
class IdentifierRegistry:
    """
    Client identities are composed of a unique combination of multiple
    client identifiers. A specific identifier may be shared by one or
    client identities. For example, a married couple sharing a single
    email address.
    """
    def __init__(self):
        """
        Create a new client identity registry.
        """
        # Class attributes.
        self.identifier_list = {}

    def add_identifier(self, identifier):
        """
        Add a new client identifier to the client identifier registry
        and update the identifiers registry with the new client id info.
        """
        if not identifier.key in self.identifier_list.items():
            self.identifier_list[identifier.key] = identifier

    def save_identifier_client_idno(self, identifier_key, client_idno):
        """
        Add client idno to the identifier's set of id numbers.
        """
        identifier = self.identifier_list[identifier_key]
        identifier.save_client_idno(client_idno)