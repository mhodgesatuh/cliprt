#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
import re

class ClientIdentifier:
    """
    Each client's identity is comprised of a unique set of client
    identifiers.
    """
    def __init__(self, de_name, de_value, ded):
        """
        Data elements are tagged as identifiers in the DED configuration
        and used to match client data to client identities.  A single
        client's information may be spread across multiple data content
        worksheets.
        """
        # Class attributes.
        self.client_ids = set()
        self.de_name = self.make_searchable(de_name)
        self.de_value = self.make_searchable(de_value)
        self.type = ded[self.de_name].get_identifier_type()
        
        # Sanitize.
        if self.type == 'phone':
            self.santize_phone_value()

        # After sanitization.    
        self.key = self.get_identifier_key()

    def __repr__(self):
        """
        Representation of the client identifier is the identifier key.
        """
        return self.key

    def get_identifier_key(self):
        """
        The identifier key is a comibination of data identifier type and
        the identifier value to ensure that there is no accidental 
        identifier value match across disparate data elements.
        """
        return '{}::{}'.format(self.type, self.de_value)

    def make_searchable(self, str_value):
        """
        Ensure that values are lowercase strings and easily searchable.
        """
        return str_value.strip().lower() \
            if isinstance(str_value, str) else str(str_value)

    def santize_phone_value(self):
        """
        Find the numberic portions of the string and join them.
        """
        self.de_value = ''.join(re.findall("\d+", self.de_value))

    def save_client_idno(self, client_idno):
        """
        Keep a running list of the client id's for which this identifier
        matches.
        """
        self.client_ids.add(client_idno)