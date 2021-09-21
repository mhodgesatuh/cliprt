#!/usr/bin/env python
"""
Project:    CLIPRT - Client Information Parsing and Reporting Tool.
@author:    mhodges
Copyright   2020 Michael Hodges
"""
import operator

class ClientIdentityResolver:
    """
    Once a row of data is processed and the identifiers isolated, the
    identifiers can then be compared to the identifier registry to 
    determine of the data matches an existing client identity or 
    belongs to a new client identity.
    """
    def __init__(self, client_registry, identifier_registry):
        """
        Create a new identity resolver.
        """
        # Dependency injections.
        self.client_reg = client_registry
        self.identifier_reg = identifier_registry

        # Class attributes.
        self.matched_identifier_types = []
        self.identifier_matched = []
        self.identifier_unmatched = []

    def assess_identifier(self, identifier):
        """
        Search for the identifier value to see if we have a potential 
        identity match. Add the identifier to the identifier registry.
        """
        if identifier.type == 'phone':
            if not self.is_useful_phone_identifier(identifier.de_value):
                # Ignore useless phone identifiers.
                return
        elif identifier.type == 'email':
            if not self.is_useful_email_identifier(identifier.de_value):
                # Ignore useless email identifiers.
                return

        if identifier.key in self.identifier_reg.identifier_list:
            self.identifier_matched.append(identifier)
            if not identifier.type in self.matched_identifier_types:
                # Track the number of unique identifier types found. 
                # It takes a minimal number to indicate an identity
                # match.
                self.matched_identifier_types.append(identifier.type)
        else:
            # Save the identifier value since it doesn't match any 
            # existing saved identifier.
            self.identifier_reg.add_identifier(identifier)
            self.identifier_unmatched.append(identifier)

    def client_idno_matcher(self, client_idno_sets):
        """
        Apply set theory to the sets containing identity data matches 
        in order to determine which existing client id is likely the 
        best match.
        """
        # Create a list of all identity numbers.
        first_idno_set = list(client_idno_sets)[0]
        idno_list = first_idno_set.union(*client_idno_sets)

        # Count the occurences of each identity number across all sets 
        # of identity numbers.
        idno_match_cnt = {}
        for idno in idno_list:

            # Initialize the count for each identity number.
            idno_match_cnt[idno] = 0

            # Render it as a set in order to compare to the identity 
            # number sets.
            idno_match_set = {idno}

            # Count number of sets in which the identity number is 
            # found.
            for idno_set in client_idno_sets:
                if idno_match_set.issubset(idno_set):
                    idno_match_cnt[idno]+=1

        # Sort such that the identity number with the most matches is 
        # listed first.
        sorted_idno_by_cnt = sorted(
            idno_match_cnt.items(), 
            key=operator.itemgetter(1), 
            reverse=True
            )

        # The best match client id is in the first key of the first 
        # tuple.
        return sorted_idno_by_cnt[0][0]

    def create_identity(self):
        """
        If the identifiers don't match an existing identity, per the
        registry search, this is a new identity to be add to the 
        registry.
        """
        return self.client_reg.create_identity()

    def is_useful_email_identifier(self, de_value):
        """
        Detect and reject bogus data in order to help reduce invalid
        identity matches.
        """
        if 'noemail' in de_value:
            return False
        return True

    def is_useful_phone_identifier(self, de_value):
        """
        Detect and reject bogus data in order to help reduce invalid
        identity matches.
        """
        if '0000' in de_value:
            return False
        if '9999' in de_value:
            return False
        return True

    def match_existing_identity(self):
        """
        Determine which of the client's set of identifiers matches an 
        existing identity.
        """
        client_id_sets = []
        for identifier in self.identifier_matched:
            idno_set = self.identifier_reg.identifier_list[identifier.key].client_ids
            client_id_sets.append(idno_set)
        return self.client_idno_matcher(client_id_sets)

    def resolve_client_identity(self, threshold):
        """
        Determine the client id based on the number of matched 
        identifiers.  If this is a new client id, create the new
        identifier.
        """
        if len(self.identifier_matched) == 0 and len(self.identifier_unmatched) == 0:
            # No useful identifiers provided.
            return None

        if len(self.matched_identifier_types) < threshold:
            # Too few identifiers match, so this is a new identity.
            identity = self.create_identity()
        else:
            # The identifiers match one or more existing identities.
            # Determine which is the most likely match for the 
            # current row of client data.
            client_idno = self.match_existing_identity()
            identity = self.client_reg.get_identity_by_idno(client_idno)

        # Now that we have a client id, the identifiers can be updated
        # to reflect the new client id with which they are now 
        # associated.
        for identifier in self.identifier_matched:
            identifier.save_client_idno(identity.client_idno)
        for identifier in self.identifier_unmatched:
            identifier.save_client_idno(identity.client_idno)

        return identity